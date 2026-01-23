from dataclasses import dataclass
from typing import Final, final

from vulnfinder.application.commands.knowledge_base.ensure_ready import (
    EnsureKnowledgeBaseCommand,
    EnsureKnowledgeBaseCommandHandler,
)
from vulnfinder.application.common.ports.llm_client import LlmClient
from vulnfinder.application.common.ports.vector_store import VectorStoreGateway
from vulnfinder.application.common.views.analysis_result import AnalysisResultView


@dataclass(frozen=True, slots=True, kw_only=True)
class AnalyzeCodeCommand:
    code: str
    context_query: str | None = None
    top_k: int = 5


@final
class AnalyzeCodeCommandHandler:
    def __init__(
        self,
        llm_client: LlmClient,
        vector_store: VectorStoreGateway,
        ensure_kb: EnsureKnowledgeBaseCommandHandler,
    ) -> None:
        self._llm_client: Final[LlmClient] = llm_client
        self._vector_store: Final[VectorStoreGateway] = vector_store
        self._ensure_kb: Final[EnsureKnowledgeBaseCommandHandler] = ensure_kb
        self._kb_max_age_days: Final[int] = 7

    def __call__(self, data: AnalyzeCodeCommand) -> AnalysisResultView:
        if self._ensure_kb is not None and self._vector_store is not None:
            self._ensure_kb(
                EnsureKnowledgeBaseCommand(max_age_days=self._kb_max_age_days)
            )

        context_texts: list[str] = []
        if self._vector_store is not None and data.context_query:
            results = self._vector_store.similarity_search(data.context_query, data.top_k)
            context_texts = [doc.content for doc in results]

        prompt = self._build_prompt(data.code, context_texts)
        response = self._llm_client.invoke(prompt)
        return AnalysisResultView(raw_response=response, context_used=context_texts)

    @staticmethod
    def _build_prompt(code: str, contexts: list[str]) -> str:
        if not contexts:
            return f"Analyze the following code for vulnerabilities.\n\n{code}"

        joined_context = "\n\n".join(contexts)
        return (
            "You are a security analyzer. Use the context to detect vulnerabilities.\n\n"
            f"Context:\n{joined_context}\n\n"
            f"Code:\n{code}"
        )
