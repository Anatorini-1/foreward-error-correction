from util import Util as ut
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
            blocks = ut.partition(data, 2**(param)-param-1)
            res = []
            for block in blocks:
                res.append(self.hamming(block, param))
            return ut.unPartition(res)
        elif code is self.CYCLIC:
            return self.cyclic(data, param)
        elif code is self.BLOCK:
            return self.block(data, param)
        elif code is self.REPEAT:
            blocks = ut.partition(data, 1)
            blocks = [self.repeat(block, param) for block in blocks]
            return ut.unPartition(blocks)
        elif code is self.SINGLE_PARITY:
            blocks = ut.partition(data, param)
            return [self.single_parity(block) for block in blocks]
        elif code is self.BCH:
            return self.bch(data, param)
        elif code is self.REED_SOLOMON:
            return self.reed_solomon(data, param)
        elif code is self.REED_SOLOMON_2:
            return self.reed_solomon_2(data, param)
        else:
            return data

    def hamming(self, data: list, redundancy: int) -> list:
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

    def block(self, data, block_size):
        pass

    def repeat(self, bit, n):
        """Encodes the data by repeating each bit n times

        Args:
            bit (list): list of bits to encode
            n (int): number of times to repeat each bit

        Returns:
            list: list of bits, with each bit repeated n times
        """
        return bit*n

    def single_parity(self, data):
        """Encodes the data by appending a parity bit to the end of the data

        Args:
            data (list): list of bits to encode

        Returns:
            list: list of bits, with a parity bit appended to the end
        """
        data.append(sum(data) % 2)
        return data

    def bch(self, data, n):
        pass

    def reed_solomon(self, data, n):
        pass

    def reed_solomon_2(self, data, n):
        pass

    def cyclic(self, data, n):
        pass
