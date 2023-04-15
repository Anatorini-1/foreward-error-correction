from flask import *
from flask_cors import CORS
from encoder import encoder, encodings as enc
from decoder import decoder
from channel import channel
from util import Util as ut
import json
import imageio
import struct
en = encoder()
ch = channel()
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


@app.route("/api/send", methods=["POST"])
def send():
    jsonData = json.loads(request.data)
    print(jsonData)
    encoding = jsonData['encoding']
    params = jsonData["encodingParams"]
    data = jsonData["data"]
    type = jsonData["type"]
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
    binaryData = serializeData(data, type)
    binaryData = ut.unPartition(binaryData)
    encodedData = en.encode(binaryData, enc[encoding], paramsToPass)
    encodedData = ut.unPartition(encodedData)
    noisyData = ch.send(encodedData)
    decodedData = dc.decode(noisyData, enc[encoding], paramsToPass)
    # using binaryData as a placeholder
    formattedData = deserializeData(binaryData, type)
    return json.dumps({
        "data": formattedData,
        "bitsSent": len(encodedData),
        "code": "200",
        "totalErrors": 0,  # TODO to be supplied by channel
        "correctedErrors": 0,  # TODO to be supplied by decoder
        "BER": 1  # TODO to be supplied by channel and decoder combined
    }), 200


def serializeData(data: any, dataType: str) -> list:
    """Turns suported data types into a list of bits

    Args:
        data (any): data to serialize
        dataType (str): type of data

    Returns:
        list: list of bits representing the data
    """

    chars = [ord(char) for char in data]
    bits = ut.decListToBinaryList(chars)
    return bits


def deserializeData(data: list, dataType: str) -> any:
    """Turns a list of bits into a supported data type

    Args:
        data (list): list of bits
        dataType (str): type of data

    Returns:
        any: reconstucted data
    """
    charCodes = ut.binaryListToDec(data)
    chars = [chr(code) for code in charCodes]
    text = "".join(chars)
    return text
