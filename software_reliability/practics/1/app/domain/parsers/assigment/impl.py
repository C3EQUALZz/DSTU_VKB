import ast
from typing import Any, override

from app.domain.parsers.visitor.impl import BaseAnalyzer


class AssignmentMixin(BaseAnalyzer):
    @override
    def visit_Assign(self, node: ast.Assign) -> Any:
        if any(hasattr(target, 'annotation') for target in node.targets):
            self.generic_visit(node)
            return

        self._stats["assignments"] += 1
        self._operators["Присваивание"].append((self._current_line, node.col_offset))
        self.generic_visit(node)

    @override
    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        self.generic_visit(node)
