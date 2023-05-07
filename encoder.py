from util import Util
import komm as km
import numpy as np

# TODO add more encoders
# TODO comment code
# TODO improve readability

encodings = {
    "HAMMING": 0,
    "CYCLIC": 1,
    "REPEAT": 3,
    "BCH": 5,
    "REED_SOLOMON": 6,
    "REED_SOLOMON_2": 7
}


class encoder:
    # Enum of the different types of codes
    HAMMING = 0  # param = redundancy
    REPEAT = 3  # param = amount of times to repeat each bit
    BCH = 5  # param = n
    REED_MULLER = 6  # param = n
    REED_SOLOMON_2 = 7  # param = n
    ut = Util()

    def __init__(self):
        pass

    def encode(self, data: list, code: int, param=None) -> list:
        """Encodes the data using the specified code

        Args:
            data (list): list of bits to encode
            code (int): encoding to be used. See the enum for the different types
            param (any, optional): Encoding parameters, if any. Defaults to None.


        Returns:
            list: list of lists, each inner list is a codeword
        """
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

    def hamming(self, data: list, redundancy: int) -> list:
        blocks = self.ut.partition(data, 2**(redundancy)-redundancy-1)
        res = []
        for block in blocks:
            res.append(self.__hamming_word(block, redundancy))
        return self.ut.flatten(res)

    def repeat(self, data, n):
        """Encodes the data by repeating each bit n times

        Args:
            bit (list): list of bits to encode
            n (int): number of times to repeat each bit

        Returns:
            list: list of bits, with each bit repeated n times
        """
        blocks = self.ut.partition(data, 1)
        blocks = [block*n for block in blocks]
        return self.ut.flatten(blocks)

    def bch(self, data, n):
        """Encodes the given sequence of bits(data) with the BCH code

        Args:
            data (list): List of bits to encode
            n (tuple(int,int)): Params of the code, (μ,τ). The resulting code will have 
            a codeword length = 2^(μ - 1) and will be able to correct (at least) τ errors / codeword
        """
        code = km.BCHCode(n[0], n[1])
        encodedData = [code.encode(word)
                       for word in self.ut.partition(data, code.dimension)]
        return self.ut.flatten(encodedData)

    def reed_muller(self, data, n):
        """Encodes a given sequence of data using tj Reed-Muller
        error correction code.

        Args:
            data (list): list of bits [0,1] to encode
            n (tuple(int,int))): parameters of the code, [rho,mu] ,where 0 <= rho < mu
        """
        mu = n[0]
        rho = n[1]
        code = km.ReedMullerCode(mu, rho)
        l = code.dimension
        blocks = self.ut.partition(data, l, True)
        encoded = [code.encode(block) for block in blocks]
        return self.ut.flatten(encoded, True)

    def __hamming_word(self, data, redundancy):
        """Encodes the data using the hamming code.

        Args:
            data (list): list of bits to encode. Must be the length of one codeword worth of data.
            redundancy (int): amount of redundancy bits per codeword. Must be less than the length of the data.

        Returns:
            list: codeword representing the data, with the redundancy bits
        """
        blockLen = 2**redundancy - 1
        dataLen = blockLen-redundancy
        keys = [x for x in range(1, blockLen+1)]
        parityKeys = [2**x for x in range(redundancy)]
        dataKeys = [x for x in keys if x not in parityKeys]
        codeWord = [2 for _ in range(blockLen)]
        for i in range(dataLen):
            codeWord[dataKeys[i]-1] = data[i]
        for i in parityKeys:
            sum = 0
            for k in keys:
                if k & i:
                    sum += codeWord[k-1]
            codeWord[i-1] = sum % 2

        return codeWord
