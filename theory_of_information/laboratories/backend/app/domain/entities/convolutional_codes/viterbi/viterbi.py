from collections import namedtuple
from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.entities.convolutional_codes.viterbi.bindata import BinData
from app.domain.entities.convolutional_codes.viterbi.helpers import bits_count, conv_parity, hamming_distance

# stav[3][0/1] = (new_state, parity)  # named tuples used - Edge(new_state, parity)
Edge = namedtuple('Edge', 'new_state, parity')
INF = float('inf')


class Node:
    def __init__(self, metric=INF, bindata=None):
        self.metric = metric
        self.bindata = bindata or BinData(0, 0)

@dataclass(eq=False)
class Transitions(BaseEntity):
    """docstring for Transitions"""
    polynomials: list[int]

    def __post_init__(self) -> None:
        super().__post_init__()

        self.n_state_bits = bits_count(max(self.polynomials)) - 1
        self.n_states = 2 ** self.n_state_bits
        self.polynomials = self.polynomials
        self.parity_len = len(self.polynomials)  # length of the parity per one data bit
        self.states = [
            [
                Edge(new_state=((i_state << 1) & (2 ** self.n_state_bits - 1)) | bit,
                     parity=conv_parity(i_state << 1 | bit, self.polynomials))
                for bit in range(2)
            ]
            for i_state in range(self.n_states)
        ]


    def __str__(self):
        output = ''
        for i, state in enumerate(self.states):
            state_code = '{{:0{}b}}'.format(self.n_state_bits).format(i)
            lines = [
                ' --{{}}/{{:0{}b}}--> {{:0{}b}}\n'.format(self.parity_len, self.n_state_bits).format(b, state[b].parity,
                                                                                                     state[b].new_state)
                for b in (0, 1)]
            output += state_code + lines[0] + ' ' * len(state_code) + lines[1] + '\n'
        return output

    def generate_parities(self, bindata):
        """ Returns generator that gives (encoding) parity checks for input data """
        # It starts with most significant bits in data, going to least significant
        state = 0
        for i in reversed(range(bindata.len)):
            bit = bindata[i]
            yield self.states[state][bit].parity
            state = self.states[state][bit].new_state

    def encode(self, bindata):
        """ Encodes data using convolutional code. Public method (API). """
        parity_sequence = BinData(0, 0)
        for parity in self.generate_parities(bindata):
            parity_sequence += BinData(parity, self.parity_len)
        return parity_sequence

    def extract_parity_sequence(self, parity_sequence_bindata):
        """ Returns generator iterating through parities in parity sequence (encoded data). """
        parity_mask = (1 << self.parity_len) - 1
        parity_selector = parity_sequence_bindata.len  # number of least signifficant bits to be discarded (>>) for parity to be readable by parity_mask
        while parity_selector:
            parity_selector -= self.parity_len
            yield (parity_sequence_bindata.num & (parity_mask << parity_selector)) >> parity_selector

    def decode(self, parity_sequence_bindata):
        """ Decodes convolutional code using the Viterbi algorithm. Public method (API). """
        gen = self.extract_parity_sequence(parity_sequence_bindata)
        state = 0  # initial state

          # constant definition

        # init trellis
        olds = [Node(INF, BinData(0, 0)) for i in range(self.n_states)]  # aktualna metrika, data bits
        news = [Node(None, None) for i in range(self.n_states)]  # nova metrika, data bits (with added one new bit)
        olds[0].metric = 0  # set metrics of first state to 0

        # iterate through parities in encoded data (parity sequence)
        for parity in gen:
            # initialize news
            for new in news:
                new.metric = INF  # set new PM to infinity

            # choose best paths for new step
            for i in range(self.n_states):
                for bit in (0, 1):
                    t = self.states[i][bit].new_state
                    p = self.states[i][bit].parity
                    hd = hamming_distance(p, parity)

                    new_PM = olds[i].metric + hd  # compute candidate PM
                    if new_PM < news[t].metric:  # if this new candidate is better than existing new candidate
                        news[t].metric = new_PM
                        news[t].bindata = olds[i].bindata + bit

            # update "column" in trellis with best paths chosen in previous step and prepare for next iteration
            for i in range(self.n_states):
                olds[i].metric = news[i].metric
                olds[i].bindata = news[i].bindata

        # Finalization
        # Get state with best PM
        best_state, best_PM = None, INF
        for old in olds:
            if old.metric < best_PM:
                best_PM = old.metric
                best_state = old

        # Decoded databits:
        return best_state.bindata
