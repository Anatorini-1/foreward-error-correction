import encoder as en
import decoder as de
import channel as ch
from util import Util as ut
import komm as km
import numpy as np
import os

encoder = en.encoder()
decoder = de.decoder()


data = [1, 1, 1, 1, 1, 1]
print(data)
codeWords = encoder.encode(data, encoder.REPEAT, 3)
decodedData = decoder.decode(codeWords, decoder.REPEAT, 3)

print(decodedData)
