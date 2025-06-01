import ast
from typing import Protocol, Any


class IAssignmentHandler(Protocol):
    def visit_Assign(self, node: ast.Assign) -> Any: ...

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any: ...
