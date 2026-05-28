"""Чтение строк из текстового файла (по одной на строку)."""

from pathlib import Path

from steganography.domain.linguistic_bit_in_string.ports.string_reader import (
    StringReader,
)


class FileStringReader(StringReader):
    """Возвращает непустые строки файла, очищенные от концевых пробелов."""

    def read(self, path: Path) -> list[str]:
        raw = path.read_text(encoding="utf-8").splitlines()
        return [line.rstrip() for line in raw if line.strip()]
