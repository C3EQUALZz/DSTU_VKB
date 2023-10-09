from string import ascii_lowercase as low, ascii_uppercase as up

class CaesarCipher:
    def __init__(self, key):
        self._encode = str.maketrans(low, low[key:] + low[:key]) | str.maketrans(up, up[key:] + up[:key])
        self._decode = {v: k for k, v in self._encode.items()}

    def encode(self, string):
        return str.translate(string, self._encode)

    def decode(self, string):
        return str.translate(string, self._decode)
