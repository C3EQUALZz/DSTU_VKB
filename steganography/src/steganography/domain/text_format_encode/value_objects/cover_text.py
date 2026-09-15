"""Cover text, line boundaries and an optional original DOCX snapshot.

Plain-text covers use the base font settings. DOCX covers retain the source
package so the writer can preserve each run's formatting and document layout.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CoverText:
    """Строки контейнера и базовый шрифт для воссоздания разметки."""

    lines: tuple[str, ...]
    font_name: str | None = None
    font_size: str | None = None  # размер в half-points OOXML (напр. "39")

    source_docx: bytes | None = field(default=None, repr=False)

    @classmethod
    def from_plain(cls, text: str) -> CoverText:
        """Из плоской строки: переносы \\n становятся границами строк."""
        return cls(lines=tuple(text.split("\n")))

    @property
    def text(self) -> str:
        """Плоский поток видимых символов (без границ строк)."""
        return "".join(self.lines)

    @property
    def line_lengths(self) -> tuple[int, ...]:
        """Длины строк в символах — по ним писатель режет план."""
        return tuple(len(line) for line in self.lines)
