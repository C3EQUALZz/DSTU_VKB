from typing import Protocol

from app.domain.entities.viterbi.bindata import BinData


class ConvolutionalCoderProtocol(Protocol):
    def encode(self, bindata: BinData):
        ...

    def decode(self, parity_sequence_bindata):
        ...
