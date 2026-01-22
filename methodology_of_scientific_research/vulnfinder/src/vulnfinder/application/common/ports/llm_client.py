from abc import abstractmethod
from typing import Protocol


class LlmClient(Protocol):
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        raise NotImplementedError

