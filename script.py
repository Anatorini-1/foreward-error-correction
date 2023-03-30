import encoder as en
import decoder as de
import channel as ch
from util import Util as ut
import komm as km
import numpy as np
encoder = en.encoder()
decoder = de.decoder()
channel = ch.channel()

img = ut.readImage("img.bmp")
flatImg = ut.flattenImage(img)
binImage = ut.decToBinaryList(flatImg)
decImage = ut.binaryListToDec(binImage)
rgbImage = ut.unFlattenImage(decImage, 100, 100)
ut.writeImage("img3.bmp", rgbImage)
