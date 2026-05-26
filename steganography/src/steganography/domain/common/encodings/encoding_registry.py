"""Реестр всех поддерживаемых кодировок."""

from steganography.domain.common.encodings.ascii_encoding import (
    AsciiEncoding,
)
from steganography.domain.common.encodings.baudot_mtk2_encoding import (
    BaudotMtk2Encoding,
)
from steganography.domain.common.encodings.encoding import Encoding
from steganography.domain.common.encodings.fixed_width_encoding import (
    FixedWidthEncoding,
)


class EncodingRegistry:
    """Каталог кодировок, известных декодеру.

    Используется доменом вместо прямого импорта констант — позволяет
    добавлять новые кодировки расширением реестра без правки сервисов
    (принцип Open-Closed).
    """

    def __init__(self) -> None:
        self._mtk2: Encoding = BaudotMtk2Encoding()
        self._koi8r: Encoding = FixedWidthEncoding(name="КОИ-8R", codec="koi8-r")
        self._cp866: Encoding = FixedWidthEncoding(name="cp866", codec="cp866")
        self._win1251: Encoding = FixedWidthEncoding(name="Windows-1251", codec="windows-1251")
        self._ascii: Encoding = AsciiEncoding()

    def all(self) -> tuple[Encoding, ...]:
        return (self._mtk2, self._koi8r, self._cp866, self._win1251, self._ascii)

    def by_name(self, name: str) -> Encoding | None:
        for encoding in self.all():
            if encoding.name == name:
                return encoding
        return None

    def names(self) -> tuple[str, ...]:
        return tuple(encoding.name for encoding in self.all())

    @property
    def mtk2(self) -> Encoding:
        return self._mtk2
