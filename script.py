import encoder as en
import decoder as de
import channel as ch
from util import Util as ut
import komm as km
import numpy as np
import os
from PIL import Image
encoder = en.encoder()
decoder = de.decoder()


bits = ut.readImageToBinary("./img/20x20.bmp")
encoded = encoder.bch(bits, (7, 20))
decoded = decoder.decode(encoded, decoder.BCH, (7, 20))
img = ut.creteImageFromBinary(decoded, 20, 20)
img.show()
