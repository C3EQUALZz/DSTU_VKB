from langchain_core.language_models import BaseChatModel

from vulnfinder.application.common.ports.llm_client import LlmClient


class LangChainLlmClient(LlmClient):
    def __init__(self, client: BaseChatModel) -> None:
        self._client = client

    def invoke(self, prompt: str) -> str:
        response = self._client.invoke(prompt)
        return response.content
