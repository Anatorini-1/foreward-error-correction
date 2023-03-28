import imageio
import numpy as np


class Util:

    # Reads the @file_name image and returns it as a numpy array (width x height x 3)
    @staticmethod
    def readImage(file_name):
        img = imageio.imread(file_name)
        return img

    # Writes the @img numpy array to the @file_name image
    @staticmethod
    def writeImage(file_name, img):
        imageio.imwrite(file_name, img)
        return

    # Flatterns the @img numpy array to a list of rgb values
    @staticmethod
    def flattenImage(img):
        result = []
        for row in img:
            for pixel in row:
                for channell in pixel:
                    result.append(channell)
        return result

    @staticmethod
    def unFlattenImage(img, width, height):
        result = []
        for i in range(height):
            row = []
            for j in range(width):
                pixel = []
                for k in range(3):
                    pixel.append(img[i * width * 3 + j * 3 + k])
                row.append(pixel)
            result.append(row)
        return result

    @staticmethod
    def partition(data, n):
        result = []
        toApp = max(n-1, len(data) % n)
        for i in range(toApp):
            data.append(0)

        blockCount = int(len(data)/n)
        blockLen = int(len(data)/blockCount)
        for i in range(0, blockCount):
            result.append(data[blockLen * i: blockLen * (i+1)])
        return result

    @staticmethod
    def unPartition(data):
        return np.array(data).flatten().tolist()

    @staticmethod
    def intToBin(n) -> int:
        result = ""
        while n > 0:
            result = str(n % 2) + result
            n = n // 2
        return int(result)

    @staticmethod
    def swapEncoding(data: list, method="canonical") -> str:
        newData = [0 for x in range(len(data))]
        keys = [x for x in range(1, len(data)+1)]
        redundancyBits = int(np.ceil(np.log2(len(data))))
        parityKeys = [2**x for x in range(redundancyBits)]
        dataKeys = [x for x in keys if x not in parityKeys]
        i = 0
        if method == "canonical":
            # from [data_segment, parity_segment] to data and parity mixed,
            # parity bits have indexes 2^i-1
            for key in dataKeys:
                newData[key-1] = data[i]
                i += 1
            for key in parityKeys:
                newData[key-1] = data[i]
                i = i+1
        elif method == "data_parity":
            # from canonical to [data_segment, parity_segment]
            for key in dataKeys:
                newData[i] = data[key-1]
                i = i+1
            for key in parityKeys:
                newData[i] = data[key-1]
                i = i+1
        return newData
