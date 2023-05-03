from encoder import encoder, encodings as enc
from decoder import decoder
from channel import channel
from util import Util as ut
import matplotlib.pyplot as plt
from PIL import Image


def calculateErrors(input: list, output: list) -> int:
    errors = 0
    for i in range(len(input)):
        if input[i] != output[i]:
            errors = errors + 1
    return errors


def test_repeat():
    data = ut.readImageToBinary(R"C:\Users\stani\Desktop\proba.png")

    enValues = [2, 3, 4, 5, 6]
    x = []  # redundancja
    y = []  # błedy na koniec / pierwotna dlugosc wiadomosci
    en = encoder()
    for val in enValues:
        encodedData = en.encode(data, 3, val)
        ch = channel(encodedData)
        ch.random_errors(0.2)
        dec = decoder()
        decodedData = dec.decode(ch.output_bits, 3, val)
        x.append(len(encodedData) / len(data))  # dopisuje obecna redundancje
        y.append(float(calculateErrors(data, decodedData) / len(data)))
    plt.plot(x, y)
    plt.show()
    # resultImage = ut.creteImageFromBinary(decodedData, 100, 100)
    # resultImage.show()


def test_hamming():
    data = ut.readImageToBinary(R"C:\Users\stani\Desktop\proba.png")

    enValues = [3]
    x = []  # redundancja
    y = []  # błedy na koniec / pierwotna dlugosc wiadomosci
    en = encoder()
    for val in enValues:
        encodedData = en.encode(data, 0, val)
        ch = channel(encodedData)
        ch.random_errors(0.2)
        dec = decoder()
        decodedData = dec.decode(ch.output_bits, 0, 3)
        x.append(len(encodedData) / len(data))  # dopisuje obecna redundancje
        y.append(float(calculateErrors(data, decodedData) / len(data)))
    plt.plot(x, y)
    plt.show()


#test_repeat()
test_hamming()