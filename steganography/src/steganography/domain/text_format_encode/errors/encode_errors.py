"""Доменные ошибки встраивания сокрытия."""


class EncodeError(Exception):
    """Базовая ошибка процесса встраивания."""


class ContainerTooSmallError(EncodeError):
    """Контейнер короче, чем требуется для размещения полезной нагрузки."""

    def __init__(self, required_bits: int, available_chars: int) -> None:
        self.required_bits = required_bits
        self.available_chars = available_chars
        super().__init__(
            f"контейнеру нужно минимум {required_bits} символов, "
            f"доступно {available_chars}",
        )


class UnencodableSecretError(EncodeError):
    """Секретный текст невозможно представить в выбранной кодировке."""

    def __init__(self, encoding_name: str) -> None:
        self.encoding_name = encoding_name
        super().__init__(
            f"секретное сообщение не кодируется в «{encoding_name}»",
        )
