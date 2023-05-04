from encoder import encoder, encodings as enc
from decoder import decoder
from channel import channel
from util import Util as ut
import matplotlib.pyplot as plt
from PIL import Image

repeatEncodingParams = [1, 2, 3, 4, 5, 6]
blockEncodingParams = [1, 2, 3, 4, 5, 6]
hammingEncodingParams = [3, 4, 5, 6]
bchEncodingParams = [3, 4, 5, 6]
reedSolomonEncodingParams = [2, 3, 4, 5, 6]  # TODO: sprawdzic jakie parametry powinny byc testowane


# nie bedzie dzialac dla hamminga bo dane input są dłuższe niż dane output przez dodanie zer
def calculateErrors(input: list, output: list) -> int:
    errors = 0
    for i in range(len(input)):
        if input[i] != output[i]:
            errors = errors + 1
    return errors


# TODO: switch case dla różnych modeli
# models parameters:
# 1 = random errors
# 2 = group noises
# 3 = gilbert_eliot_model

def test_repeat(model, encodingParams):
    data = ut.readImageToBinary(R"C:\Users\stani\Desktop\proba.png")
    x = []  # redundancja
    y = []  # błedy na koniec / pierwotna dlugosc wiadomosci
    en = encoder()
    for val in encodingParams:
        encodedData = en.encode(data, 3, val)

        ch = channel(encodedData)
        if model == 0:
            ch.random_errors(0.4)
        elif model == 1:
            ch.group_noise(2, 10)
        elif model == 2:
            pass  # ch.gilbert_elliot_model(0.1, )

        dec = decoder()
        decodedData = dec.decode(ch.output_bits, 3, val)
        x.append(len(encodedData) / len(data))  # dopisuje obecna redundancje
        y.append(float(calculateErrors(data, decodedData) / len(data)))
    plt.plot(x, y)
    plt.show()
    # resultImage = ut.creteImageFromBinary(decodedData, 100, 100)
    # resultImage.show()

# block code nie jest jeszcze napisany
def test_block(model, encodingParams):
    data = ut.readImageToBinary(R"C:\Users\stani\Desktop\proba.png")
    x = []  # redundancja
    y = []  # błedy na koniec / pierwotna dlugosc wiadomosci
    en = encoder()
    for val in encodingParams:
        encodedData = en.encode(data, 2, val)

        ch = channel(encodedData)
        if model == 0:
            ch.random_errors(0.4)
        elif model == 1:
            ch.group_noise(2, 10)
        elif model == 2:
            pass  # ch.gilbert_elliot_model(0.1, )

        dec = decoder()
        decodedData = dec.decode(ch.output_bits, 2, val)
        x.append(len(encodedData) / len(data))  # dopisuje obecna redundancje
        y.append(float(calculateErrors(data, decodedData) / len(data)))
    plt.plot(x, y)
    plt.show()
    # resultImage = ut.creteImageFromBinary(decodedData, 100, 100)
    # resultImage.show()    #

def test_hamming(channelModel, encodingParams):
    data = ut.readImageToBinary(R"C:\Users\stani\Desktop\proba.png")
    cpyData = data.copy()

    x = []  # redundancja
    y = []  # błedy na koniec / pierwotna dlugosc wiadomosci
    en = encoder()
    for val in encodingParams:
        print('redundancy: ', val)
        print('data',
              len(data))  # TODO: kodowanie wiadomosci wydluza ją zapełaniając zerami brakujące miejsca, ale dlaczego dla redundancji 4 giną 2 bity
        encodedData = en.encode(data, 0, val)
        print('encodedData', len(encodedData))

        ch = channel(encodedData)
        if channelModel == 0:
            ch.random_errors(0.2)
        elif channelModel == 1:
            ch.group_noise(2, 8)
        elif channelModel == 2:
            pass  # ch.gilbert_elliot_model(0.1, )

        dec = decoder()
        decodedData = dec.decode(ch.output_bits, 0, val)
        x.append(len(encodedData) / len(data))  # dopisuje obecna redundancje

        print('encoding reverted', (len(encodedData) / (2 ** val - 1)) * (2 ** val - 1 - val))
        print('decoded', len(decodedData))
        print('\n')
        # y.append(float(calculateErrors(data, decodedData) / len(data)))
    # plt.plot(x, y)
    # plt.show()

def test_bch(channelModel, encodingParams):
    data = ut.readImageToBinary(R"C:\Users\stani\Desktop\proba.png")
    cpyData = data.copy()

    x = []  # redundancja
    y = []  # błedy na koniec / pierwotna dlugosc wiadomosci
    en = encoder()
    for val in encodingParams:
        print('data', len(data))
        encodedData = en.encode(data, 5, val)

        ch = channel(encodedData)
        if channelModel == 0:
            ch.random_errors(0.2)
        elif channelModel == 1:
            ch.group_noise(2, 8)
        elif channelModel == 2:
            pass  # ch.gilbert_elliot_model(0.1, )

        dec = decoder()
        decodedData = dec.decode(ch.output_bits, 5, val)
        x.append(len(encodedData) / len(data))  # dopisuje obecna redundancje

        print('decoded', len(decodedData))
        print('\n')
        # y.append(float(calculateErrors(data, decodedData) / len(data)))
    # plt.plot(x, y)
    # plt.show()


def test_reed_solomon(channelModel, encodingParams):
    data = ut.readImageToBinary(R"C:\Users\stani\Desktop\proba.png")

    x = []  # redundancja
    y = []  # błedy na koniec / pierwotna dlugosc wiadomosci
    en = encoder()
    for val in encodingParams:
        print('data', len(data))
        encodedData = en.encode(data, 6, val)

        ch = channel(encodedData)
        if channelModel == 0:
            ch.random_errors(0.2)
        elif channelModel == 1:
            ch.group_noise(2, 8)
        elif channelModel == 2:
            pass  # ch.gilbert_elliot_model(0.1, )

        dec = decoder()
        decodedData = dec.decode(ch.output_bits, 6, val)
        x.append(len(encodedData) / len(data))  # dopisuje obecna redundancje

        print('decoded', len(decodedData))
        print('\n')
        # y.append(float(calculateErrors(data, decodedData) / len(data)))
    # plt.plot(x, y)
    # plt.show()


# test_repeat(1, repeatEncodingParams)
test_block(1, blockEncodingParams)
# test_hamming(1, hammingEncodingParams)
