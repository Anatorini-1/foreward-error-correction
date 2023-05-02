from util import Util as ut
import komm as km
import numpy as np

encodings = {
    "HAMMING": 0,
    "CYCLIC": 1,
    "REPEAT": 3,
    "BCH": 5,
    "REED_SOLOMON": 6,
    "REED_SOLOMON_2": 7
}


class decoder:
    # Enum of the different types of codes
    HAMMING = 0  # param = redundancy
    CYCLIC = 1  # param = n
    BLOCK = 2   # param = n
    # param = block_size (1 does nothing, 2 repeats each bit onece, and so on)
    REPEAT = 3  # param = amount of times to repeat each bit
    SINGLE_PARITY = 4  # Param = amount of data bits per codeword
    BCH = 5  # param = n
    REED_SOLOMON = 6  # param = n
    REED_SOLOMON_2 = 7  # param = n

    def __init__(self):
        pass

    def decode(self, data: list, code: int, param=None) -> list:
        if code is self.HAMMING:
            return self.hamming(data, param)
        elif code is self.CYCLIC:
            return self.cyclic(data, param)
        elif code is self.BLOCK:
            return self.block(data, param)
        elif code is self.REPEAT:
            blocks = ut.partition(data, param)
            blocks = [self.repeat(block, param) for block in blocks]
            return blocks
        elif code is self.BCH:
            return self.bch(data, param)
        elif code is self.REED_SOLOMON:
            return self.reed_solomon(data, param)
        elif code is self.REED_SOLOMON_2:
            return self.reed_solomon_2(data, param)
        else:
            return data

    def hamming(self, codeData: list, redundancy: int) -> list:
        code = km.HammingCode(redundancy)
        wordLen = 2**(redundancy)-1
        codeWords = ut.partition(codeData, wordLen)
        codeWords = [ut.swapEncoding(c, "data_parity") for c in codeWords]
        decodedData = [code.decode(cw) for cw in codeWords]
        return ut.flatten(decodedData)

    def block(self, data, block_size):
        pass

    def repeat(self, block, n):
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

    def bch(self, data, param):
        pass

    def reed_solomon(self, data, n):
        pass

    def reed_solomon_2(self, data, n):
        pass

    def cyclic(self, data, n):
        pass
