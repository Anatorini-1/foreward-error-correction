from flask import *
from flask_cors import CORS
from encoder import encoder, encodings as enc
from decoder import decoder
from channel import channel
from util import Util as ut
import json

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
    encoding = request.data["encoding"]
    params = request.data["params"]
    data = request.data["data"]
    type = request.data["type"]

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

    paramsToPass = json.loads(params)
    if encoding == "HAMMING":  # TODO add more encodings
        paramsToPass = int(paramsToPass)

    binaryData = serializeData(data, type)
    encodedData = en.encode(binaryData, enc[encoding], paramsToPass)
    noisyData = ch.send(encodedData)
    decodedData = dc.decode(noisyData, enc[encoding], paramsToPass)
    formattedData = deserializeData(decodedData, type)
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
    if dataType == "plainText":
        chars = [ord(char) for char in data]
        bits = ut.decListToBinaryList(chars)
        return ut.unPartition(bits)
    elif dataType == "img":
        return [0, 0, 0, 0, 0, 0, 0, 0]  # TODO
    elif dataType == "textFile":
        return [0, 0, 0, 0, 0, 0, 0, 0]  # TODO
    else:
        return data


def deserializeData(data: list, dataType: str) -> any:
    """Turns a list of bits into a supported data type

    Args:
        data (list): list of bits
        dataType (str): type of data

    Returns:
        any: reconstucted data
    """

    if dataType == "plainText":
        charCodes = ut.binaryListToDec(data)
        chars = [chr(code) for code in charCodes]
        text = "".join(chars)
        return text
    elif dataType == "img":
        return [0, 0, 0, 0, 0, 0, 0, 0]  # TODO
    elif dataType == "textFile":
        return [0, 0, 0, 0, 0, 0, 0, 0]  # TODO

    return data
