from util import Util
import komm as km
import numpy as np

encodings = {
    "HAMMING": 0,
    "CYCLIC": 1,
    "REPEAT": 3,
    "BCH": 5,
    "REED_MULLER": 6,
}


class decoder:
    # Enum of the different types of codes
    HAMMING = 0  # param = redundancy
    # param = block_size (1 does nothing, 2 repeats each bit onece, and so on)
    REPEAT = 3  # param = amount of times to repeat each bit
    BCH = 5  # param = n
    REED_MULLER = 6  # param =

    ut = Util()

    def __init__(self):
        pass

    def decode(self, data: list, code: int, param=None) -> list:
        if code is self.HAMMING:
            return self.hamming(data, param)
        elif code is self.REPEAT:
            return self.repeat(data, param)
        elif code is self.BCH:
            return self.bch(data, param)
        elif code is self.REED_MULLER:
            return self.reed_muller(data, param)
        else:
            return data

    def hamming(self, codeData: list, redundancy: int) -> list:
        code = km.HammingCode(redundancy)
        wordLen = 2**(redundancy)-1
        codeWords = self.ut.partition(codeData, wordLen)
        codeWords = [self.ut.swapEncoding(c, "data_parity") for c in codeWords]
        decodedData = [code.decode(cw) for cw in codeWords]
        return self.ut.flatten(decodedData)

    def repeat(self, data, n):
        blocks = self.ut.partition(data, n)
        blocks = [self.repeat_block(block, n) for block in blocks]
        return blocks

    def repeat_block(self, block, n):
        zero_count = 0
        one_count = 0
        for bit in block:
            if bit == 0:
                zero_count += 1
            elif bit == 1:
                one_count += 1
        if zero_count < one_count:
            return 1
        else:
            return 0

    def bch(self, data, params: tuple):
        """Decodes the given sequence of bits(data)

        Args:
            data (list): List of bits to decode
            params (tuple(int,int)): Params used to encode the data (μ,τ).
        """
        code = km.BCHCode(params[0], params[1])
        decodedData = [code.decode(word)
                       for word in self.ut.partition(data, code.length)]
        return self.ut.flatten(decodedData)

    def reed_muller(self, data, n):
        """Decodes a given sequence of data using tj Reed-Muller
        error correction code.

        Args:
            data (list): list of bits [0,1] to decode
            n (tuple(int,int))): parameters of the code, [rho,mu] ,where 0 <= rho < mu
        """
        mu = n[0]
        rho = n[1]
        code = km.ReedMullerCode(mu, rho)
        l = code.length
        blocks = self.ut.partition(data, l)
        encoded = [code.decode(block) for block in blocks]
        return self.ut.flatten(encoded)
