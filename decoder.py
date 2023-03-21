class decoder:
    def __init__(self):
        pass

    def decode(self, data, key):
        return data[:-len(key)]
