import re
from dataclasses import dataclass

from typing_extensions import override

from cryptography_methods.domain.ceaser.errors import BadKeyForCaesarKeywordError
from cryptography_methods.domain.common.values import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class KeyCeaserKeyword(BaseValueObject):
    k: int
    keyword: str
    m: int

    @override
    def _validate(self) -> None:
        if self.k is None or not isinstance(self.k, int):
            raise TypeError("k must be an integer")

        if self.keyword is None or not isinstance(self.keyword, str):
            raise TypeError("keyword must be a string")

        if self.keyword.isspace() or self.keyword == "":
            raise BadKeyForCaesarKeywordError("Keyword is empty, please provide some info")

        if re.search(r"\d", self.keyword) is not None:
            raise BadKeyForCaesarKeywordError("Keyword cant contain a number, please provide only letters")

        if self.m < 0:
            raise BadKeyForCaesarKeywordError("m must be positive integer")

        if not 0 <= self.k < self.m - 1:
            raise BadKeyForCaesarKeywordError("k must be between 0 and m - 1")

        if any(map(lambda x: x.isspace(), self.keyword)):
            raise BadKeyForCaesarKeywordError("Keyword must be a single word")

    @override
    def __str__(self) -> str:
        return f"{self.k=}-{self.keyword=}"
