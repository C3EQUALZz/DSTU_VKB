from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnalysisResultView:
    raw_response: str
    context_used: list[str]

