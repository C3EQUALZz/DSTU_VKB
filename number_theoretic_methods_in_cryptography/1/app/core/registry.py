from collections import deque
from typing import Final, Iterable


class LogRegistry:
    """
    Реестр, который будет просто собирать логи и отдавать их на отображение.
    """

    def __init__(self) -> None:
        self._logs: Final[deque[str]] = deque()

    def add_log(self, message: str) -> None:
        """
        Метод для добавления лога в реестр.
        """
        self._logs.append(message + "\n")

    def clear_logs(self) -> None:
        """
        Удалить все логи.
        """
        self._logs.clear()

    @property
    def logs(self) -> Iterable[str]:
        """
        Получить все логи.
        """
        return self._logs.copy()
