import encoder as en
import decoder as de
import channel as ch
from util import Util as ut
import komm as km
import numpy as np
encoder = en.encoder()
decoder = de.decoder()
channel = ch.channel()

x = [0, 0, 1, 1]
x = encoder.encode(x, encoder.HAMMING, 2)
print(x)
x = [ut.swapEncoding(x, "data_parity") for x in x]
x = ut.unPartition(x)
print(x)
