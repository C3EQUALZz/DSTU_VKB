from app.domain.entities.convolutional_codes.viterbi import Transitions
from app.domain.entities.convolutional_codes.viterbi.bindata import BinData


class ConvolutionalCodesService:
    @staticmethod
    def __ones_count(number):
        """ Returns the number of binary 1s in the number. """
        number = int(number)  # make a copy
        ones = 0
        while number:
            ones += number & 1
            number >>= 1
        return ones

    def __make_pols_list(self, arg):
        pols = [int(pol, 2) for pol in arg.split(',')]
        if min(map(self.__ones_count, pols)) < 2:
            raise ValueError(f'Every valid polynomial must have at least two binary 1s: {pols}')
        return pols

    def encode(self, data: str, pols: str) -> str:

        pols_list = self.__make_pols_list(pols)

        return str(Transitions(polynomials=pols_list).encode(BinData(data)))

    def decode(self, data: str, pols: str) -> str:
        pols_list = self.__make_pols_list(pols)

        if len(data) % len(pols_list):
            raise ValueError(
                'Decoding error: The number of data bits ({}) is not multiple of the number of polynomials ({})!'.format(
                    len(data), len(pols_list))
            )

        return str(Transitions(polynomials=pols_list).decode(BinData(data)))
