from random import random


class channel:
    def __init__(self):
        self.__error_rate = 0.5
        self.__error = 0.5
        self.__correct = 0
        self.__total = 0
        self.__error_list = []
        self.__correct_list = []
        self.__total_list = []
        self.__error_rate_list = []

    def send(self, data):
        self.__total += 1
        if random() < self.__error_rate:
            self.__error += 1
            self.__error_list.append(data)
            return self.__error_list[-1]
        else:
            self.__correct += 1
            self.__correct_list.append(data)
            return self.__correct_list[-1]
