from typing import cast

import numpy as np


class InterleaveService:
    @staticmethod
    def execute(data: np.ndarray[np.ndarray[str]]) -> np.ndarray[np.ndarray[str]]:
        return cast(np.ndarray[np.ndarray[str]], np.transpose(data))
