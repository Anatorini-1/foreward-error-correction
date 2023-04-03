import imageio
import numpy as np
from typing import List


class Util:

    @staticmethod
    def readImage(file_name: str) -> np.ndarray:
        """Reads the file_name image and returns it as a numpy array (width x height x 3)

        Args:
            file_name (str): Name of the image file

        Returns:
            np.ndarray: numpy array of the image
        """
        img = imageio.imread(file_name)
        return img

    @staticmethod
    def writeImage(file_name: str, img: np.ndarray) -> None:
        """Writes the img numpy array to the file_name image

        Args:
            file_name (str): Name of the image file
            img (np.ndarray): numpy array of the image
        """
        imageio.imwrite(file_name, img)
        return

    @staticmethod
    def flattenImage(img: np.ndarray) -> list:
        """Flattens the img numpy array to a list of rgb values

        Args:
            img (np.ndarray): numpy array of the image

        Returns:
            list: list of rgb values
        """
        result = []
        for row in img:
            for pixel in row:
                for channell in pixel:
                    result.append(channell)
        return result

    @staticmethod
    def unFlattenImage(img: np.ndarray, width: int, height: int) -> List[list]:
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
    def partition(data, n) -> List[list]:
        """Partitions the data into n blocks

        Args:
            data (list): data to partition
            n (int): length of each block

        Returns:
            List[list]: list of blocks
        """
        result = []
        if(len(data) < n):
            toApp = max(n-1, len(data) % n)
        else:
            toApp = len(data) % n
        for i in range(toApp):
            data.append(0)

        blockCount = int(len(data)/n)
        blockLen = int(len(data)/blockCount)
        for i in range(0, blockCount):
            result.append(data[blockLen * i: blockLen * (i+1)])
        return result

    @staticmethod
    def unPartition(data: List[list]) -> list:
        """Unpartitions the data into a single list (flattens the list)

        Args:
            data (List[list]): list of blocks to unpartition

        Returns:
            list: flattened list
        """
        return np.array(data).flatten().tolist()

    @staticmethod
    def intToBin(n: int) -> str:
        """Converts an integer to its binary representation

        Args:
            n (int): integer to convert

        Returns:
            str: binary representation of n
        """
        result = ""
        while n > 0:
            result = str(n % 2) + result
            n = n // 2
        if result == "":
            result = "0"
        return result

    @staticmethod
    def swapEncoding(data: list, method="canonical") -> str:
        """Swaps the Hamming encoding convention from [data_segment, parity_segment] to data and parity mixed,

        Args:
            data (list): codeword to convert
            method (str, optional): The convenction to convert to. Either "canonical" or "data_parity". Defaults to "canonical".

        Returns:
            str: converted codeword
        """
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

    @staticmethod
    def decListToBinaryList(dec: list) -> list:
        """Converts a list of decimal[0-255] values to a list of binary values

        Args:
            dec (list): list of rgb values

        Returns:
            list: list of binary values
        """
        result = []
        for value in dec:
            binValue = Util.intToBin(value)
            if(len(binValue) < 8):
                binValue = "0" * (8-len(binValue)) + binValue
            result.append([int(b) for b in binValue])
        return result

    @staticmethod
    def binaryListToDec(bin: list) -> list:
        """Converts a list of 8-bit binary values to a list of decimal values

        Args:
            bin (list): list of binary values

        Returns:
            list: list of decimal values
        """
        result = []
        bin = Util.partition(bin, 8)
        for value in bin:
            decValue = 0
            for i in range(len(value)):
                decValue += value[i] * 2**(7-i)
            result.append(decValue)
        return result
