from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnalysisResultView:
    raw_response: str
    context_used: list[str]
    analysis_run_id: str | None = None
    code_artifact_id: str | None = None
    model_session_id: str | None = None
    model_request_id: str | None = None
    model_response_id: str | None = None
