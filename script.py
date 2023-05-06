import encoder as en
import decoder as de
import channel as ch
from util import Util
import komm as km
import numpy as np
import os
from PIL import Image
encoder = en.encoder()
decoder = de.decoder()
ut = Util()

bits = ut.readImageToBinary("./img/20x20.bmp")
print(len(bits))
encoded = encoder.bch(bits, (3, 3))
print(len(encoded))
decoded = decoder.bch(encoded, (3, 3))
print(len(decoded))
img = ut.creteImageFromBinary(decoded, 20, 20)
img.show()
