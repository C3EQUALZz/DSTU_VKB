from dataclasses import dataclass, field

from vulnfinder.domain.common.entities.base_aggregate import BaseAggregateRoot
from vulnfinder.domain.common.entities.base_entity import BaseEntity
from vulnfinder.domain.llm_analysis.value_objects.identifiers import (
    ModelRequestId,
    ModelResponseId,
    ModelSessionId,
)
from vulnfinder.domain.llm_analysis.value_objects.types import ModelName, Prompt, Temperature, TokenUsage


@dataclass(eq=False, kw_only=True)
class ModelRequest(BaseEntity[ModelRequestId]):
    prompt: Prompt
    model_name: ModelName
    temperature: Temperature | None = None


@dataclass(eq=False, kw_only=True)
class ModelResponse(BaseEntity[ModelResponseId]):
    content: str
    usage: TokenUsage | None = None


@dataclass(eq=False, kw_only=True)
class ModelSession(BaseAggregateRoot[ModelSessionId]):
    requests: list[ModelRequest] = field(default_factory=list)
    responses: list[ModelResponse] = field(default_factory=list)

    def add_request(self, request: ModelRequest) -> None:
        self.requests.append(request)

    def add_response(self, response: ModelResponse) -> None:
        self.responses.append(response)

