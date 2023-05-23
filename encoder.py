from util import Util
import komm as km
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import os
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
    ut = Util()
    tpe: ThreadPoolExecutor

    def __init__(self):
        self.tpe = ThreadPoolExecutor(os.cpu_count())
        pass

    def processChunk(self, chunk: list) -> list:
        return [self.code.encode(c) for c in chunk]

    def encode(self, data: list, codeName: int, param=None) -> list:
        """Encodes the data using the specified code

        Args:
            data (list): list of bits to encode
            code (int): encoding to be used. See the enum for the different types
            param (any, optional): Encoding parameters, if any. Defaults to None.


        Returns:
            list: list of lists, each inner list is a codeword
        """

        if codeName is self.HAMMING:
            code = self.hamming(data, param)
        elif codeName is self.REPEAT:
            code = self.repeat(data, param)
        elif codeName is self.BCH:
            code = self.bch(data, param)
        elif codeName is self.REED_MULLER:
            code = self.reed_muller(data, param)

        return self.ut.flatten([code.encode(x) for x in self.ut.partition(data, code.dimension)])

    def hamming(self, data: list, redundancy: int) -> list:
        return km.HammingCode(redundancy)

    def repeat(self, data, n):
        return km.RepetitionCode(n)

    def bch(self, data, n):
        return km.BCHCode(n[0], n[1])

    def reed_muller(self, data, n):

        mu = n[0]
        rho = n[1]
        return km.ReedMullerCode(mu, rho)

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
