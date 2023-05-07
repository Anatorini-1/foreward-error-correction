from encoder import encoder, encodings as enc
from decoder import decoder
from channel import channel
from util import Util
import matplotlib.pyplot as plt
from PIL import Image

repeatEncodingParams = [1, 2, 3, 4, 5, 6, 7]
hammingEncodingParams = [2, 3, 4, 5, 6, 7, 8]
bchEncodingParams = [[7, 15], [7, 21]]
reedMullerEncodingParams = [[2, 4], [1, 3], [1, 5], [1, 7], ]  # TODO: sprawdzic jakie parametry powinny byc testowane

random_errors_param = 0.2
group_noise_param1 = 2   # size of group
group_noise_param2 = 8   # space between groups
gilbert_eliot_param = (0.1, 0.2, 0.3, 0.4)  # TODO: sprawdzic jakie powinny byc paramatery


def calculateErrors(input: list, output: list) -> int:
    errors = 0
    for i in range((len(input))):

        if input[i] != output[i]:
            errors = errors + 1
    return errors


# models parameters:
# 0 = random errors
# 1 = group noises
# 2 = gilbert_eliot_model

def test_repeat(channelModel, encodingParams):
    ut = Util()
    data = ut.readImageToBinary(R"C:\Users\stani\Desktop\proba.png")
    x = []  # redundancy
    y = []  # BER
    en = encoder()
    temp = []
    title = ''
    for val in encodingParams:  # outer loop iterates over list of encoding parameters
        for i in range(0, 1):  # inner loop performs 3 times test for each parameter
            encodedData = en.encode(data, 3, val)

            ch = channel(encodedData)
            if channelModel == 0:
                ch.random_errors(random_errors_param)
                title = 'Repeat code, random errors channel'
            elif channelModel == 1:
                ch.group_noise(group_noise_param1, group_noise_param2)
                title = 'Repeat code, group noise channel'
            elif channelModel == 2:
                pass  # ch.gilbert_elliot_model(0.1, )
            dec = decoder()
            decodedData = dec.decode(ch.output_bits, 3, val)
            temp.append(float(calculateErrors(data, decodedData) / len(data)))  # adding result of current test to temp

        x.append(len(encodedData) / len(data))  # appending current redundancy
        y.append(float(sum(temp) / len(temp)))  # appending avg value of 10 tests
        plt.text((len(encodedData) / len(data)) + 0.2, (float(sum(temp) / len(temp))), val)

    plt.title(title)
    plt.xlabel('redundancy')
    plt.ylabel('EBR')
    plt.scatter(x, y)
    plt.show()
    # resultImage = ut.creteImageFromBinary(decodedData, 100, 100)
    # resultImage.show()


def test_hamming(channelModel, encodingParams):
    ut = Util()
    data = ut.readImageToBinary(R"C:\Users\stani\Desktop\proba.png")
    x = []  # redundancy
    y = []  # BER
    en = encoder()
    temp = []
    title = ''
    for val in encodingParams:  # outer loop iterates over list of encoding parameters
        for i in range(0, 1):  # inner loop performs 3 times test for each parameter
            encodedData = en.encode(data, 0, val)

            ch = channel(encodedData)
            if channelModel == 0:
                ch.random_errors(random_errors_param)
                title = 'Hamming code, random errors channel'
            elif channelModel == 1:
                ch.group_noise(group_noise_param1, group_noise_param2)
                title = 'Hamming code, group noise channel'
            elif channelModel == 2:
                pass  # ch.gilbert_elliot_model(0.1, )
            dec = decoder()
            decodedData = dec.decode(ch.output_bits, 0, val)
            temp.append(float(calculateErrors(data, decodedData) / len(data)))  # adding result of current test to temp

        x.append(len(encodedData) / len(data))  # appending current redundancy
        y.append(float(sum(temp) / len(temp)))  # appending avg value of 10 tests
        plt.text((len(encodedData) / len(data)) + 0.03, (float(sum(temp) / len(temp))), val)

    plt.title(title)
    plt.xlabel('redundancy')
    plt.ylabel('EBR')
    plt.scatter(x, y)
    plt.show()


# nie dziala
def test_bch(channelModel, encodingParams):
    ut = Util()
    data = ut.readImageToBinary(R"C:\Users\stani\Desktop\proba2.png")
    x = []  # redundancy
    y = []  # BER
    en = encoder()
    temp = []
    title = ''
    for val in encodingParams:  # outer loop iterates over list of encoding parameters
        encodedData = en.encode(data, 5, val)
        for i in range(0, 1):  # inner loop performs 3 times test for each parameter
            print('testing bch', val, 'for ', i, ' time')

            ch = channel(encodedData)
            if channelModel == 0:
                ch.random_errors(random_errors_param)
                title = 'BCH code, random errors channel'
            elif channelModel == 1:
                ch.group_noise(group_noise_param1, group_noise_param2)
                title = 'BCH code, group noise channel'
            elif channelModel == 2:
                pass     # ch.gilbert_elliot_model(0.1, )
            dec = decoder()
            decodedData = dec.decode(ch.output_bits, 5, val)
            temp.append(float(calculateErrors(data, decodedData) / len(data)))  # adding result of current test to temp

        x.append(len(encodedData) / len(data))  # appending current redundancy
        y.append(float(sum(temp) / len(temp)))  # appending avg value of 10 tests
        plt.text((len(encodedData) / len(data)) + 0.02, (float(sum(temp) / len(temp))), val)

    plt.title('BCH code')
    plt.xlabel('redundancy')
    plt.ylabel('EBR')
    plt.scatter(x, y)
    plt.show()


def test_reed_muller(channelModel, encodingParams):
    ut = Util()
    data = ut.readImageToBinary(R"C:\Users\stani\Desktop\proba.png")
    x = []  # redundancy
    y = []  # BER
    en = encoder()
    temp = []
    title =''
    for val in encodingParams:  # outer loop iterates over list of encoding parameters
        encodedData = en.encode(data, 6, val)
        for i in range(0, 1):  # inner loop performs 3 times test for each parameter
            print('testing reed-muller', val, 'for ', i, ' time')

            ch = channel(encodedData)
            if channelModel == 0:
                ch.random_errors(random_errors_param)
                title = 'Reed-Muller code, random errors channel'
            elif channelModel == 1:
                ch.group_noise(group_noise_param1, group_noise_param2)
                title = 'Reed-Muller code, group noise channel'
            elif channelModel == 2:
                pass  # ch.gilbert_elliot_model(0.1, )
            dec = decoder()
            decodedData = dec.decode(ch.output_bits, 6, val)
            temp.append(float(calculateErrors(data, decodedData) / len(data)))  # adding result of current test to temp

        x.append(len(encodedData) / len(data))  # appending current redundancy
        y.append(float(sum(temp) / len(temp)))  # appending avg value of 10 tests
        plt.text((len(encodedData) / len(data))+0.2, (float(sum(temp) / len(temp))), val)
    plt.title(title)
    plt.xlabel('redundancy')
    plt.ylabel('EBR')
    plt.scatter(x, y)
    plt.show()


test_repeat(0, repeatEncodingParams)
# test_hamming(1, hammingEncodingParams)
# test_hamming(0, hammingEncodingParams)
# test_bch(1, bchEncodingParams)
# test_reed_muller(0, reedMullerEncodingParams)
