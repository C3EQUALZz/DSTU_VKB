import unittest

import numpy as np

from ..help_functions import *


class TestUpShiftFunction(unittest.TestCase):

    def setUp(self):
        self.matrix = np.array(
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ]
        )

    def test_up_shift_first_column(self):
        expected_result = np.array(
            [
                [4, 2, 3],
                [7, 5, 6],
                [1, 8, 9]
            ])
        self.assertTrue(np.array_equal(up_shift_column(self.matrix.copy(), 0, 1), expected_result))

    def test_up_shift_second_column(self):
        expected_result = np.array(
            [
                [1, 5, 3],
                [4, 8, 6],
                [7, 2, 9]
            ]
        )
        self.assertTrue(np.array_equal(up_shift_column(self.matrix.copy(), 1, 1), expected_result))

    def test_up_shift_negative_positions(self):
        expected_result = np.array(
            [
                [7, 2, 3],
                [1, 5, 6],
                [4, 8, 9]
            ]
        )
        self.assertTrue(np.array_equal(up_shift_column(self.matrix.copy(), 0, -1), expected_result))


if __name__ == '__main__':
    unittest.main()
