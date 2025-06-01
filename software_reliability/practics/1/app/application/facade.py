import ast
import os
from pathlib import Path
from typing import Final

from app.application.analyzers.base import IAnalyzerComponent


class FacadeAnalyzer:
    def __init__(
            self,
            path: Path,
            analyzer: IAnalyzerComponent,
            result_path_dir: Path | None = None
    ) -> None:
        self._path: Final[Path] = path
        self._analyzer: Final[IAnalyzerComponent] = analyzer

        condition: bool = result_path_dir is not None and path.is_dir()
        self._result_path: Final[Path] = result_path_dir if condition else path.parent / "result"

    def analyze(self) -> None:
        if not os.path.isfile(self._path):
            raise FileNotFoundError(f"Файл не найден: {self._path}")

        with open(self._path, "r", encoding="utf-8") as source:
            try:
                tree: ast.Module = ast.parse(source.read(), filename=self._path)
            except SyntaxError as e:
                raise RuntimeError(f"Ошибка синтаксиса в файле: {self._path}") from e

        self._analyzer.visit(tree)
