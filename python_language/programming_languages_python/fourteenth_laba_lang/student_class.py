"""
Реализация класса Student
"""
__all__ = ['Student']

from dataclasses import dataclass

import numpy as np


@dataclass
class Student:
    last_name: str
    initials: str
    number_group: int
    grades: np.ndarray[float, ...]

