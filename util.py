import imageio
import numpy as np
from typing import List
from PIL import Image


class Util:
    paddingLen: int = 0

    def partition(self, data: list, n: int, respectPadding: bool = True) -> List[list]:
        """Partitions the data into n-long blocks

        Args:
            data (list): data to partition
            n (int): length of each block

        Returns:
            List[list]: list of blocks
        """

        if len(data) % n != 0:
            toAdd = (n - (len(data) % n))
            data = data + [0]*toAdd
            if respectPadding:
                self.paddingLen = toAdd

        blocks = []
        for i in range(0, int(len(data)/n)):
            s = i*n
            end = s+n
            blocks.append(data[s:end])
        return blocks

    def flatten(self, data: List[list], respectPadding: bool = True) -> list:
        """Unpartitions the data into a single list (flattens the list)

        Args:
            data (List[list]): list of blocks to unpartition

        Returns:
            list: flattened list
        """

        toReturn = np.array(data).flatten().tolist()
        if respectPadding:
            toReturn = toReturn[0:len(toReturn) - self.paddingLen]
            self.paddingLen = 0
        return toReturn

    def intToBin(self, n: int) -> str:
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

    def swapEncoding(self, data: list, method="canonical") -> str:
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

    def decListToBinaryList(self, dec: list) -> list:
        """Converts a list of decimal[0-255] values to a list of binary values

        Args:
            dec (list): list of rgb values

        Returns:
            list: list of binary values
        """
        result = []
        for value in dec:
            binValue = self.intToBin(value)
            if(len(binValue) < 8):
                binValue = "0" * (8-len(binValue)) + binValue
            result.append([int(b) for b in binValue])
        return result

    def binaryListToDec(self, bin: list) -> list:
        """Converts a list of 8-bit binary values to a list of decimal values

        Args:
            bin (list): list of binary values

        Returns:
            list: list of decimal values
        """
        result = []
        bin = self.partition(bin, 8)
        for value in bin:
            decValue = 0
            for i in range(len(value)):
                decValue += value[i] * 2**(7-i)
            result.append(int(decValue))
        return result

    def readImageToBinary(self, fileName: str) -> list:
        """Reads the fileName image and returns it as a 1-D array of bits, 
        representing the size of imgWidth*imgHeight*3(RGB) * 8 (bits per RGB value)

        Args:
            fileName (str): path to the image

        Returns:
        list: list of bits representing the image
        """
        img = Image.open(fileName, 'r', formats=None)
        pixelArray = list(img.getdata())
        pixelArray = self.flatten(pixelArray)
        binaryArray = self.decListToBinaryList(pixelArray)
        binaryArray = self.flatten(binaryArray)
        return binaryArray

    def creteImageFromBinary(self, bits: list, width: int, height: int) -> Image:
        """Turn a binary representation of and image and transforms it to a PIL(library) Image

        Args:
            bits (list): BInary representation of an image (1-D array of 1s and 0s)
            width (int): width of an image
            height (int): height of an image

        Returns:
            Image: Image object created from the binary representation
        """
        rgb = self.binaryListToDec(bits)
        pixels = self.partition(rgb, 3)
        pixels = [tuple(p) for p in pixels]
        img = Image.new("RGB", (width, height))
        img.putdata(pixels)
        return img

