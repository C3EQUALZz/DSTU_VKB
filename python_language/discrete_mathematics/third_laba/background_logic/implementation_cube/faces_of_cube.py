"""
Здесь у меня будут находиться грани кубика
Удобно их задать через перечисления мои костлявые
"""
import numpy as np


class CubeSide:
    __slots__ = ("UP", "LEFT", "FRONT", "RIGHT", "BACK", "DOWN")

    def __init__(self, block):
        self.UP = np.array([list(block[i:i + 3]) for i in range(0, 9, 3)], dtype=np.dtype('b'))
        self.LEFT = np.array([list(block[i + 9:i + 12]) for i in range(0, 33, 12)], dtype=np.dtype('b'))
        self.FRONT = np.array([list(block[i + 12:i + 15]) for i in range(0, 33, 12)], dtype=np.dtype('b'))
        self.RIGHT = np.array([list(block[i + 15:i + 18]) for i in range(0, 33, 12)], dtype=np.dtype('b'))
        self.BACK = np.array([list(block[i + 18:i + 21]) for i in range(0, 33, 12)], dtype=np.dtype('b'))
        self.DOWN = np.array([list(block[i:i + 3]) for i in range(45, 54, 3)], dtype=np.dtype('b'))
