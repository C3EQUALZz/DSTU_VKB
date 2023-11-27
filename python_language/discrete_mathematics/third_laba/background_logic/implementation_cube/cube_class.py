import numpy as np
from .faces_of_cube import CubeSide


class Cube:
    dimensions = 3

    def __init__(self, block):
        assert len(block) == 54
        self.UP = CubeSide.UP
        self.LEFT = CubeSide.LEFT
        self.FRONT = CubeSide.FRONT
        self.RIGHT = CubeSide.RIGHT
        self.BACK = CubeSide.BACK
        self.DOWN = CubeSide.DOWN

    def rot_x(self, prime=False):
        '''
        Rotates the entire cube on R face.
        Anticlockwise rotation is simply clockwise rotation * 3
        '''
        for i in range(3 if prime else 1):
            bufU = self.UP
            self.UP = self.FRONT
            self.FRONT = self.DOWN
            self.DOWN = self.BACK[::-1, ::-1]
            self.BACK = bufU[::-1, ::-1]
            self.RIGHT = np.rot90(self.RIGHT, k=-1)
            self.LEFT = np.rot90(self.LEFT, k=1)

    def rot_y(self, prime=False):
        '''Rotates the entire cube on U face.
        Anticlockwise rotation is simply clockwise rotation * 3
        '''
        for i in range(3 if prime else 1):
            bufF = self.FRONT
            self.FRONT = self.RIGHT
            self.RIGHT = self.BACK
            self.BACK = self.LEFT
            self.LEFT = bufF
            self.UP = np.rot90(self.UP, k=-1)
            self.DOWN = np.rot90(self.DOWN, k=1)

    def rot_F(self, prime=False):
        '''Rotates face F
        Anticlockwise rotation is simply clockwise rotation * 3
        '''
        self.FRONT = np.rot90(self.FRONT, k=1 if prime else -1)

        for i in range(3 if prime else 1):
            buf = self.LEFT[:, -1].copy()
            self.LEFT[:, -1] = self.DOWN[0]
            self.DOWN[0] = self.RIGHT[:, 0][::-1]
            self.RIGHT[:, 0] = self.UP[-1]
            self.UP[-1] = buf[::-1]

    # We define all other face rotations as combinations of x y and F

    def rot_B(self, prime=False):
        # B = 2y F 2y
        # B' = 2y F' 2y
        self.rot_y()
        self.rot_y()
        self.rot_F(prime)
        self.rot_y()
        self.rot_y()

    def rot_L(self, prime=False):
        # L = y' F y
        # L'= y' F' y
        self.rot_y(True)
        self.rot_F(prime)
        self.rot_y()

    def rot_R(self, prime=False):
        # R = y F y'
        # R'= y F' y'
        self.rot_y()
        self.rot_F(prime)
        self.rot_y(True)

    def rot_U(self, prime=False):
        # U = x' F x
        # U' = x' F' x
        self.rot_x(True)
        self.rot_F(prime)
        self.rot_x()

    def rot_D(self, prime=False):
        # D = x F x'
        # D' = x F' x'
        self.rot_x()
        self.rot_F(prime)
        self.rot_x(True)

    def apply(self, move, prime=False):
        getattr(self, "rot_" + move[0])(prime)

    def scramble(self, scramble):
        # Take each move and apply it, if it contains a'2', do it again
        for move in scramble.split(' '):
            m = move.replace("2", "")
            self.apply(m, "'" in move)
            if '2' in move:
                self.apply(m, "'" in move)

    def unscramble(self, scramble):
        # Take the reversed move list, if no '2' in move, do the reverse, other
        for move in scramble.split(' ')[::-1]:
            m = move.replace("2", "")
            self.apply(m, "'" not in move)
            if '2' in move:
                self.apply(m, "'" not in move)

    def get_block_bytes(self):
        out = b"".join(self.UP.flatten())
        out += b"".join(np.array(list(zip(self.LEFT, self.FRONT, self.RIGHT, self.BACK))).flatten())
        out += b"".join(self.DOWN.flatten())
        return out

    def __str__(self):
        indent = ' ' * self.dimensions + ' ' * (self.dimensions - 1) + '\t'

        out = indent
        out += '\n{i}'.format(i=indent).join([' '.join([tile for tile in row]) for row in self.UP]) + '\n\n'
        out += "\n".join(
            ["\t".join([" ".join(r) for r in x]) for x in np.array(list(zip(self.LEFT, self.FRONT, self.RIGHT, self.BACK)))])
        out += "\n\n"
        out += indent
        out += '\n{i}'.format(i=indent).join([' '.join([tile for tile in row]) for row in self.DOWN]) + '\n'
        return out
