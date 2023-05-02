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
img = ut.creteImageFromBinary(bits, 20, 20)
img.show()
