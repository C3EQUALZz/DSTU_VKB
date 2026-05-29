"""MarkerPackager — оборачивание полезной нагрузки маркерами начала/конца.

Маркеры выполняют ту же роль, что в методичке Mathcad: чётко отделяют
шифротекст от случайного шума LSB-битов, не относящихся к сообщению.
"""

from typing import Final, final

from steganography.domain.lsb_bmp_vigenere.errors.lsb_errors import (
    MarkersNotFoundError,
)

_DEFAULT_START_MARKER: Final[bytes] = b"n0G@m0k"
_DEFAULT_END_MARKER: Final[bytes] = b"KiHeu,6"


@final
class MarkerPackager:
    """Сервис обёртки/распаковки байтового сообщения метками."""

    def __init__(
        self,
        start_marker: bytes = _DEFAULT_START_MARKER,
        end_marker: bytes = _DEFAULT_END_MARKER,
    ) -> None:
        self._start: Final[bytes] = start_marker
        self._end: Final[bytes] = end_marker

    @property
    def start_marker(self) -> bytes:
        return self._start

    @property
    def end_marker(self) -> bytes:
        return self._end

    def pack(self, payload: bytes) -> bytes:
        return self._start + payload + self._end

    def unpack(self, stream: bytes) -> bytes:
        start_index = stream.find(self._start)
        if start_index < 0:
            raise MarkersNotFoundError
        end_index = stream.find(self._end, start_index + len(self._start))
        if end_index < 0:
            raise MarkersNotFoundError
        return stream[start_index + len(self._start) : end_index]
