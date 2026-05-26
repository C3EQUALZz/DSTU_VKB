"""ASCII — 7- или 8-битное латинское кодирование без расширения кириллицы."""

from dataclasses import dataclass

from steganography.domain.common.encodings.encoding import Encoding


@dataclass(frozen=True)
class AsciiEncoding(Encoding):
    """ASCII-кодировка. Принимает 8-битные байты, символы вне 0–127 запрещены."""

    name: str = "ASCII"

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
        if any(b > 0x7F for b in data):
            return None
        try:
            return data.decode("ascii")
        except UnicodeDecodeError:
            return None

    def encode(self, text: str) -> str | None:
        try:
            data: bytes = text.encode("ascii")
        except UnicodeEncodeError:
            return None
        return "".join(f"{byte:08b}" for byte in data)
