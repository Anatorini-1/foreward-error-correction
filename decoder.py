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
            code = self.hamming(data, param)
        elif code is self.REPEAT:
            code = self.repeat(data, param)
        elif code is self.BCH:
            code = self.bch(data, param)
        elif code is self.REED_MULLER:
            code = self.reed_muller(data, param)
        return self.ut.flatten([code.decode(x) for x in self.ut.partition(data, code.length)])

    def hamming(self, data: list, redundancy: int) -> list:
        return km.HammingCode(redundancy)

    def repeat(self, data, n):
        return km.RepetitionCode(n)

    def bch(self, data, params: tuple):

        return km.BCHCode(params[0], params[1])

    def reed_muller(self, data, n):

        mu = n[0]
        rho = n[1]
        return km.ReedMullerCode(mu, rho)
