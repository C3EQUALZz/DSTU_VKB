from typing import Final

from langchain_core.language_models import BaseChatModel
from typing_extensions import override

from vulnfinder.application.common.ports.llm_client import LlmClient


class LangChainLlmClient(LlmClient):
    def __init__(self, client: BaseChatModel) -> None:
        self._client: Final[BaseChatModel] = client

    @override
    def invoke(self, prompt: str) -> str:
        response = self._client.invoke(prompt)
        return response.content
