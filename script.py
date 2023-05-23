import encoder as en
import decoder as de
import channel as ch
from util import Util
import komm as km
import numpy as np
import os
from PIL import Image
import time
from tests import *
if __name__ == "__main__":

    repeatEncodingParams = [3, 5, 7, 9, 11, 13, 15, 17]
    hammingEncodingParams = [3, 4, 5, 6, 7, 8]
    bchEncodingParams = [
        (3, 1),
        (4, 1),
        (4, 2),
        (4, 3),
        (7, 10)

    ]
    reedMullerEncodingParams = [
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (1, 7),
        (1, 2),
        (2, 3),
        (2, 4),
        (3, 5),
        (3, 6),
        (5, 7)
    ]

    #test_hamming(GILBERT_ELLIOT, hammingEncodingParams)
    #test_hamming(GROUP_ERRORS, hammingEncodingParams)
    #test_hamming(RANDOM_ERRORS, hammingEncodingParams)

    test_bch(GILBERT_ELLIOT, bchEncodingParams)
    test_bch(GROUP_ERRORS, bchEncodingParams)
    test_bch(RANDOM_ERRORS, bchEncodingParams)

    #test_reed_muller(GILBERT_ELLIOT, reedMullerEncodingParams)
    #test_reed_muller(GROUP_ERRORS, reedMullerEncodingParams)
    #test_reed_muller(RANDOM_ERRORS, reedMullerEncodingParams)

    #test_repeat(RANDOM_ERRORS, repeatEncodingParams)
    #test_repeat(GROUP_ERRORS, repeatEncodingParams)
    #test_repeat(GILBERT_ELLIOT, repeatEncodingParams)
