from abc import ABCMeta, abstractmethod


class CipherABC(metaclass=ABCMeta):
    def __init__(self, key, *args, **kwargs):
        self.key = key

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @abstractmethod
    def encrypt(self, plain_text):
        pass

    @abstractmethod
    def decrypt(self, cipher_text):
        pass