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
        elif code is self.BCH:
            return self.bch(data, param)
        elif code is self.REED_SOLOMON:
            return self.reed_solomon(data, param)
        elif code is self.REED_SOLOMON_2:
            return self.reed_solomon_2(data, param)
        else:
            return data

    def hamming(self, data: list, redundancy: int) -> list:
        pass

    def bch(self, data, param):
        return km.BCHCode.decode(data)

    def reed_solomon(self, data, n):
        pass

    def reed_solomon_2(self, data, n):
        pass

    def cyclic(self, data, n):
        pass
