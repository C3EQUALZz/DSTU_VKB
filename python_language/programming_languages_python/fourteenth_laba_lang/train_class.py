"""
Реализация класса Train
"""

__all__ = ["Train"]

from dataclasses import dataclass
from arrow import Arrow


@dataclass
class Train:
    dest: str
    number: int
    departure: Arrow.time

