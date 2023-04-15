import encoder as en
import decoder as de
import channel as ch
from util import Util as ut
import komm as km
import numpy as np
import os

encoder = en.encoder()
decoder = de.decoder()
channel = ch.channel()
#code = km.HammingCode(3)
# os.system("cls")
#numbers = [x for x in range(10)]
#payload = ut.decToBinaryList(numbers)
#payload = [int(x) for x in payload]
#codeWords = encoder.encode(payload, encoder.HAMMING, 3)
#codeWords = [ut.swapEncoding(x, "data_parity") for x in codeWords]
#data = [code.decode(x) for x in codeWords]
#data = ut.unPartition(data)
#data = ut.partition(data, 8)

#data = ut.binaryListToDec(data)
# for d in data:
#    print(d, end="\n")
