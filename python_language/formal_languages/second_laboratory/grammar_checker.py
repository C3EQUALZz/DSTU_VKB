"""
Обязательно для просмотра, чтобы понимать материал:
 1. https://youtu.be/XvDdCQxCYJ0?si=jTHna1pSAHafhEVJ
 2. https://www.youtube.com/watch?v=fM5UiCAFyIU
"""

from python_language.formal_languages.first_laboratory import *
from enum import Enum


class GrammarType(Enum):
    REGULAR = 0
    CONTEXT_FREE = 1
    CONTEXT_SENSITIVE = 2
    UNDEFINED = 3


def recognize(grammar: dict[str, list[str]]) -> GrammarType:
    if is_left_linear(grammar) or is_right_linear(grammar):
        return GrammarType.REGULAR

    if is_context_free(grammar):
        return GrammarType.CONTEXT_FREE

    if is_context_sensitive(grammar):
        return GrammarType.CONTEXT_SENSITIVE

    # xAbCD -> xHD
    return GrammarType.UNDEFINED
