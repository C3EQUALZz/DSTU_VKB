from app.domain.parsers.visitor.impl import BaseAnalyzer


class DetailedCodeAnalyzer(
    BaseAnalyzer,
):
    def __init__(self) -> None:
        super().__init__()
        self._type_exclusions: set[str] = {
            'List', 'Dict', 'Set', 'Tuple',
            'Optional', 'Union', 'Type', 'Callable'
        }
