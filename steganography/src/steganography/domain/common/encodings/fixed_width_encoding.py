"""8-битная байтовая кодировка (КОИ-8R, cp866, Windows-1251)."""

from dataclasses import dataclass

from steganography.domain.common.encodings.encoding import Encoding


@dataclass(frozen=True)
class FixedWidthEncoding(Encoding):
    """Кодировка с фиксированной шириной 8 бит на символ."""

    name: str
    codec: str

    def decode(self, bits: str) -> str | None:
        usable: str = bits[: len(bits) - len(bits) % 8]
        if not usable:
            return None
        try:
            data: bytes = bytes(
                int(usable[i : i + 8], 2)
                for i in range(0, len(usable), 8)
            )
        except ValueError:
            return None
        try:
            return data.decode(self.codec)
        except UnicodeDecodeError:
            return None

    def encode(self, text: str) -> str | None:
        try:
            data: bytes = text.encode(self.codec)
        except UnicodeEncodeError:
            return None
        return "".join(f"{byte:08b}" for byte in data)
