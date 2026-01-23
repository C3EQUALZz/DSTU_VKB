from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from vulnfinder.application.commands.knowledge_base.ensure_ready import (
    EnsureKnowledgeBaseCommand,
    EnsureKnowledgeBaseCommandHandler,
)
from vulnfinder.application.common.ports.llm_client import LlmClient
from vulnfinder.application.common.ports.vector_store import VectorStoreGateway
from vulnfinder.application.common.views.analysis_result import AnalysisResultView
from vulnfinder.domain.analysis.services import AnalysisFactory
from vulnfinder.domain.analysis.value_objects.types import (
    AnalysisConfig,
    AnalysisTargetType,
)
from vulnfinder.domain.codebase.services import CodebaseFactory
from vulnfinder.domain.codebase.value_objects.types import FilePath
from vulnfinder.domain.llm_analysis.services import LlmAnalysisFactory
from vulnfinder.domain.llm_analysis.value_objects.types import ModelName, Prompt
from vulnfinder.setup.configs.open_router_config import OpenRouterConfig


@dataclass(frozen=True, slots=True, kw_only=True)
class AnalyzeCodeCommand:
    code: str
    context_query: str | None = None
    top_k: int = 5
    source_path: Path | None = None
    recursive: bool = False


@final
class AnalyzeCodeCommandHandler:
    def __init__(  # noqa: PLR0917,PLR0913
        self,
        llm_client: LlmClient,
        vector_store: VectorStoreGateway,
        ensure_kb: EnsureKnowledgeBaseCommandHandler,
        analysis_factory: AnalysisFactory,
        codebase_factory: CodebaseFactory,
        llm_analysis_factory: LlmAnalysisFactory,
        open_router_config: OpenRouterConfig,
    ) -> None:
        self._llm_client: Final[LlmClient] = llm_client
        self._vector_store: Final[VectorStoreGateway] = vector_store
        self._ensure_kb: Final[EnsureKnowledgeBaseCommandHandler] = ensure_kb
        self._analysis_factory: Final[AnalysisFactory] = analysis_factory
        self._codebase_factory: Final[CodebaseFactory] = codebase_factory
        self._llm_analysis_factory: Final[LlmAnalysisFactory] = llm_analysis_factory
        self._open_router_config: Final[OpenRouterConfig] = open_router_config
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

        analysis_config = AnalysisConfig(
            recursive=data.recursive,
            enable_rag=bool(data.context_query),
            max_files=None,
            model_name=self._open_router_config.default_model,
            language_filters=(),
        )
        analysis_run = self._analysis_factory.create_run(analysis_config)
        analysis_run.start()

        artifact_id: str | None = None
        if data.source_path is not None:
            code_artifact = self._codebase_factory.create_artifact(
                path=FilePath(value=str(data.source_path)),
                is_directory=data.source_path.is_dir(),
            )
            target_type = AnalysisTargetType(
                value="DIRECTORY" if code_artifact.is_directory else "FILE",
            )
            analysis_target = self._analysis_factory.create_target(
                path=code_artifact.path,
                target_type=target_type,
            )
            analysis_run.add_target(analysis_target)
            analysis_run.add_task(self._analysis_factory.create_task(analysis_target.id))
            artifact_id = str(code_artifact.id)

        prompt = self._build_prompt(data.code, context_texts)
        model_session = self._llm_analysis_factory.create_session()
        model_request = self._llm_analysis_factory.create_request(
            prompt=Prompt(value=prompt),
            model_name=ModelName(value=self._open_router_config.default_model),
        )
        model_session.add_request(model_request)

        response = self._llm_client.invoke(prompt)
        model_response = self._llm_analysis_factory.create_response(content=response)
        model_session.add_response(model_response)
        analysis_run.finish()

        return AnalysisResultView(
            raw_response=response,
            context_used=context_texts,
            analysis_run_id=str(analysis_run.id),
            code_artifact_id=artifact_id,
            model_session_id=str(model_session.id),
            model_request_id=str(model_request.id),
            model_response_id=str(model_response.id),
        )

    @staticmethod
    def _build_prompt(code: str, contexts: list[str]) -> str:
        if not contexts:
            return (
                "You are an application security analyst.\n"
                "Analyze the code for security vulnerabilities, unsafe patterns,\n"
                "and misconfigurations. Use only the provided code as evidence.\n"
                "Do not invent APIs or behavior not shown.\n\n"
                "Return the response in Russian with the following format:\n"
                "1) Summary (2-4 sentences)\n"
                "2) Findings (list; if none, say 'Нет уязвимостей')\n"
                "   - Title\n"
                "   - Severity: Critical/High/Medium/Low/Info\n"
                "   - Confidence: High/Medium/Low\n"
                "   - CWE (if known)\n"
                "   - Evidence (quote exact code snippet)\n"
                "   - Explanation (why this is vulnerable)\n"
                "   - Exploit scenario (how it could be abused)\n"
                "   - Fix (concrete, minimal change)\n"
                "3) Assumptions/Unknowns (if any)\n\n"
                "Code:\n"
                f"{code}"
            )

        joined_context = "\n\n".join(contexts)
        return (
            "You are an application security analyst.\n"
            "Use the provided context as supporting knowledge only when relevant.\n"
            "If the context conflicts with the code, trust the code.\n"
            "Do not invent APIs or behavior not shown.\n\n"
            "Return the response in Russian with the following format:\n"
            "1) Summary (2-4 sentences)\n"
            "2) Findings (list; if none, say 'Нет уязвимостей')\n"
            "   - Title\n"
            "   - Severity: Critical/High/Medium/Low/Info\n"
            "   - Confidence: High/Medium/Low\n"
            "   - CWE/CVE (if known, prefer context)\n"
            "   - Evidence (quote exact code snippet)\n"
            "   - Explanation (why this is vulnerable)\n"
            "   - Exploit scenario (how it could be abused)\n"
            "   - Fix (concrete, minimal change)\n"
            "3) Assumptions/Unknowns (if any)\n\n"
            "Context:\n"
            f"{joined_context}\n\n"
            "Code:\n"
            f"{code}"
        )
