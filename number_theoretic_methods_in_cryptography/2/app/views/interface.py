from abc import abstractmethod
from typing import Iterable, Protocol


class ViewInterface(Protocol):
    @abstractmethod
    def get_a(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_b(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_k(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_m(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_n(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_result1(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_result2(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_sum_result(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def show_logs(self, logs: Iterable[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def show_error(self, message: str) -> None:
        raise NotImplementedError
