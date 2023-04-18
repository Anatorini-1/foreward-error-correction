import numpy as np
from flask import *
from flask_cors import CORS
from encoder import encoder, encodings as enc
from decoder import decoder
from channel import channel
from util import Util as ut
import json

from PIL import Image
import base64
from io import BytesIO
import io
from time import time

en = encoder()
dc = decoder()
# For now we only support hamming-encoded plain text, but will do for now,
# gotta build the frontend first

# TODO support all encodings
# TODO support all data types
# TODO add simulation params provided by the channel/encoder/decoder
# TODO pass channel params to the channel


supportedDataTypes = ["plainText", "img", "textFile"]

app = Flask(__name__)
CORS(app)

global width, height
width = 20
height = 20


@app.route("/api/send", methods=["POST"])
def send():

    # Get the data from the request
    jsonData = json.loads(request.data)
    encoding = jsonData['encoding']
    params = jsonData["encodingParams"]
    data = jsonData["data"]
    type = jsonData["type"]
    channelType = jsonData["channelType"]
    channelParams = jsonData["channelParams"]

    # Check if the data is valid
    if encoding not in enc.keys():
        return json.dumps({
            "error": "Invalid encoding",
            "message": "The encoding you specified is not valid. Please use one of the following: " + str(enc.keys()),
            "code": "400"
        }), 400
    if type not in supportedDataTypes:
        return json.dumps({
            "error": "Invalid data type",
            "message": "The data type you specified is not valid. Please use one of the following: " + str(supportedDataTypes),
            "code": "400"
        }), 400
    if encoding == "HAMMING":  # TODO add more encodings
        paramsToPass = int(params[0])
    elif encoding == "REPEAT":
        paramsToPass = int(params[0])

    # Parse the data, turn in into a list of bits
    binaryData = serializeData(data, type)
    print("Data serialized")
    # Run the simulation
    encodedData = en.encode(binaryData, enc[encoding], paramsToPass)
    encodedData = ut.unPartition(encodedData)
    print("Data encoded")
    ch = channel(encodedData)
    addNoise(ch, channelType, channelParams)
    noisyData = ch.output_bits
    print("Data sent through channel")
    decodedData = dc.decode(noisyData, enc[encoding], paramsToPass)
    print("Data decoded")
    # Encode the data into a json response
    formattedData = deserializeData(decodedData, type)
    return json.dumps({
        "data": formattedData,
        "dataType": type,
        "dataFormat": "bmp" if type == "img" else "txt",
        "bitsSent": len(encodedData),
        "code": "200",
        "totalErrors": ch.errors,
        "correctedErrors": 0,  # TODO to be supplied by decoder
        "BER": ch.error_ratio  # TODO to be supplied by channel and decoder combined
    }), 200


def serializeData(data: any, dataType: str) -> list:
    """Turns suported data types into a list of bits

    Args:
        data (any): data to serialize
        dataType (str): type of data

    Returns:
        list: list of bits representing the data
    """
    if(dataType == "img"):
        img = stringToImg(data)
        global width, height
        width, height = img.size
        bits = imgToBits(img)

    else:
        chars = [ord(char) for char in data]
        bits = ut.decListToBinaryList(chars)
        bits = ut.unPartition(bits)

    return bits


def deserializeData(data: list, dataType: str) -> any:
    """Turns a list of bits into a supported data type

    Args:
        data (list): list of bits
        dataType (str): type of data

    Returns:
        any: reconstucted data
    """
    if dataType == "img":
        img = bitsToImg(data)
        text = imgToString(img)

    else:
        charCodes = ut.binaryListToDec(data)
        chars = [chr(code) for code in charCodes]
        text = "".join(chars)
    return text


def addNoise(ch: channel, channelType: str, channelParams: list) -> list:
    if channelType == "BinarySymetric":
        ch.random_errors(float(channelParams[0]))
    elif channelType == "GilbertElliot":
        print(channelParams)
        p1 = float(channelParams[0])
        p2 = float(channelParams[1])
        pg = float(channelParams[2])
        pb = float(channelParams[3])
        ch.gilbert_elliot_model(p1, p2, pg, pb),
        float(channelParams[3])
    pass


def parseEncodingParams(params: list) -> list:
    """Parses encoding params from a list of strings to a list of ints

    Args:
        params (list): list of strings

    Returns:
        list: list of ints
    """
    return [int(param) for param in params]


def stringToImg(data: str) -> Image:
    binary_data = io.BytesIO(data.encode("latin-1"))
    img = Image.open(binary_data)
    return img


def imgToString(img: Image) -> str:
    buffered = BytesIO()
    img.save(buffered, format="BMP")
    imageBytes = buffered.getvalue()
    b64 = base64.b64encode(imageBytes).decode("utf-8")
    return b64


def imgToBits(img: Image) -> list:
    img = img.convert("RGB")
    rgbList = list(img.getdata())
    rgbList = [item for sublist in rgbList for item in sublist]
    bits = ut.decListToBinaryList(rgbList)
    bits = ut.unPartition(bits)
    return bits


def bitsToImg(bits: list) -> Image:
    rgbList = ut.binaryListToDec(bits)
    rgbList = ut.partition(rgbList, 3)
    rgbList = [tuple(rgb) for rgb in rgbList]
    img = Image.new("RGB", (width, height))
    print(img.size[0] * img.size[1]*3)
    print(len(rgbList))
    img.putdata(rgbList)
    return img
