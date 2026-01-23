from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class ParseExtensionsQuery:
    extensions: str


class ParseExtensionsQueryHandler:
    def __call__(self, data: ParseExtensionsQuery) -> tuple[str, ...]:
        return tuple(
            ext.strip().lower() for ext in data.extensions.split(",") if ext.strip()
        )
