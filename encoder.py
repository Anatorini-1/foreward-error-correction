from util import Util as ut
import komm as km
import numpy as np


class encoder:
    # Enum of the different types of codes
    HAMMING = 0  # param = [n, k]
    CYCLIC = 1  # param = n
    BLOCK = 2   # param = n
    # param = block_size (1 does nothing, 2 repeats each bit onece, and so on)
    REPEAT = 3
    SINGLE_PARITY = 4  # This is useless for error correction, only works for error detection
    BCH = 5  # param = n
    REED_SOLOMON = 6  # param = n
    REED_SOLOMON_2 = 7  # param = n

    def __init__(self):
        pass

    def encode(self, data, code, param=None):
        # Data is a list of integers (a flattened image in the case of this project)
        # Code is an integer representing the type of code to use
        # Param is an integer or list of integers representing the parameters of the code (if any)
        if code is self.HAMMING:
            blocks = ut.partition(data, 2**(param)-param-1)
            res = []
            for block in blocks:
                res.append(self.hamming(block, param))
            return res
        elif code is self.CYCLIC:
            return self.cyclic(data, param)
        elif code is self.BLOCK:
            return self.block(data, param)
        elif code is self.REPEAT:
            return self.repeat(data, param)
        elif code is self.SINGLE_PARITY:
            return self.single_parity(data, param)
        elif code is self.BCH:
            return self.bch(data, param)
        elif code is self.REED_SOLOMON:
            return self.reed_solomon(data, param)
        elif code is self.REED_SOLOMON_2:
            return self.reed_solomon_2(data, param)
        else:
            return data

    def hamming(self, data, redundancy):
        blockLen = 2**redundancy - 1
        dataLen = blockLen-redundancy
        keys = [x for x in range(1, blockLen+1)]
        parityKeys = [2**x for x in range(redundancy)]
        dataKeys = [x for x in keys if x not in parityKeys]
        codeWord = [2 for x in range(blockLen)]
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

    def repeat(data, n):
        blocks = ut.partition(data, 1)
        for block in blocks:
            for i in range(n):
                block.append(block[0])
        return ut.unPartition(blocks)

    def single_parity(self, data, block_size):
        blocks = ut.partition(data, block_size-1)
        for block in blocks:
            block.append(sum(block) % 2)
        return ut.unPartition(blocks)

    def bch(self, data, n):
        pass

    def reed_solomon(self, data, n):
        pass

    def reed_solomon_2(self, data, n):
        pass

    def cyclic(self, data, n):
        pass
