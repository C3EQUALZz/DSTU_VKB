from typing import Final

from vulnfinder.domain.common.ports.uuid_provider import UUIDProvider
from vulnfinder.domain.common.services.base import BaseDomainService
from vulnfinder.domain.llm_analysis.entities.core import (
    ModelRequest,
    ModelResponse,
    ModelSession,
)
from vulnfinder.domain.llm_analysis.value_objects.identifiers import (
    ModelRequestId,
    ModelResponseId,
    ModelSessionId,
)
from vulnfinder.domain.llm_analysis.value_objects.types import (
    ModelName,
    Prompt,
    Temperature,
    TokenUsage,
)


class LlmAnalysisFactory(BaseDomainService):
    def __init__(self, uuid_provider: UUIDProvider) -> None:
        super().__init__()
        self._uuid_provider: Final[UUIDProvider] = uuid_provider

    def create_session(self) -> ModelSession:
        return ModelSession(
            id=ModelSessionId(value=self._uuid_provider()),
        )

    def create_request(
        self,
        prompt: Prompt,
        model_name: ModelName,
        temperature: Temperature | None = None,
    ) -> ModelRequest:
        return ModelRequest(
            id=ModelRequestId(value=self._uuid_provider()),
            prompt=prompt,
            model_name=model_name,
            temperature=temperature,
        )

    def create_response(self, content: str, usage: TokenUsage | None = None) -> ModelResponse:
        return ModelResponse(
            id=ModelResponseId(value=self._uuid_provider()),
            content=content,
            usage=usage,
        )
