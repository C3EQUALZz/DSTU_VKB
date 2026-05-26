"""МТК-2 (Бодо / ITA2) — 5-битная телеграфная кодировка с переключателями.

Используется каноническая таблица ITA2 (International Telegraph Alphabet
No. 2): два регистра — LETTERS и FIGURES — переключаются управляющими
комбинациями ``11111`` (LTRS) и ``11011`` (FIGS). Ни одна буква/цифра не
делит код с переключателями, поэтому кодирование биективно.

Кодировка работает с латиницей и цифрами (исторический алфавит Бодо).
Символы, отсутствующие в таблицах, при :meth:`encode` дают ``None``.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final

from steganography.domain.common.encodings.encoding import Encoding

_LETTERS: Final[Mapping[str, str]] = {
    "00000": "", "00100": " ", "00010": "\r", "01000": "\n",
    "11000": "A", "10011": "B", "01110": "C", "10010": "D",
    "10000": "E", "10110": "F", "01011": "G", "00101": "H",
    "01100": "I", "11010": "J", "11110": "K", "01001": "L",
    "00111": "M", "00110": "N", "00011": "O", "01101": "P",
    "11101": "Q", "01010": "R", "10100": "S", "00001": "T",
    "11100": "U", "01111": "V", "11001": "W", "10111": "X",
    "10101": "Y", "10001": "Z",
}

_FIGURES: Final[Mapping[str, str]] = {
    "00000": "", "00100": " ", "00010": "\r", "01000": "\n",
    "11000": "-", "10011": "?", "01110": ":", "10010": "$",
    "10000": "3", "10110": "!", "01011": "&", "00101": "#",
    "01100": "8", "11010": "'", "11110": "(", "01001": ")",
    "00111": ".", "00110": ",", "00011": "9", "01101": "0",
    "11101": "1", "01010": "4", "10100": "'", "00001": "5",
    "11100": "7", "01111": ";", "11001": "2", "10111": "/",
    "10101": "6", "10001": "+",
}

_SHIFT_LTRS: Final[str] = "11111"
_SHIFT_FIGS: Final[str] = "11011"


def _invert(table: Mapping[str, str]) -> Mapping[str, str]:
    inverted: dict[str, str] = {}
    for code, symbol in table.items():
        if symbol and symbol not in inverted:
            inverted[symbol] = code
    return inverted


_LETTER_CODES: Final[Mapping[str, str]] = _invert(_LETTERS)
_FIGURE_CODES: Final[Mapping[str, str]] = _invert(_FIGURES)


@dataclass(frozen=True)
class BaudotMtk2Encoding(Encoding):
    """5-битная Baudot/ITA2 (МТК-2) с переключателями LTRS/FIGS."""

    name: str = "МТК-2 (Бодо)"

    def decode(self, bits: str) -> str | None:
        usable: str = bits[: len(bits) - len(bits) % 5]
        if not usable:
            return None
        out: list[str] = []
        mode_letters: bool = True
        for i in range(0, len(usable), 5):
            code: str = usable[i : i + 5]
            if code == _SHIFT_LTRS:
                mode_letters = True
                continue
            if code == _SHIFT_FIGS:
                mode_letters = False
                continue
            table: Mapping[str, str] = _LETTERS if mode_letters else _FIGURES
            sym: str | None = table.get(code)
            if sym is None:
                return None
            out.append(sym)
        return "".join(out)

    def encode(self, text: str) -> str | None:
        out: list[str] = []
        mode_letters: bool = True
        for ch in text.upper():
            letter_code: str | None = _LETTER_CODES.get(ch)
            figure_code: str | None = _FIGURE_CODES.get(ch)
            if mode_letters and letter_code is not None:
                out.append(letter_code)
            elif not mode_letters and figure_code is not None:
                out.append(figure_code)
            elif letter_code is not None:
                out.append(_SHIFT_LTRS)
                out.append(letter_code)
                mode_letters = True
            elif figure_code is not None:
                out.append(_SHIFT_FIGS)
                out.append(figure_code)
                mode_letters = False
            else:
                return None
        return "".join(out)
