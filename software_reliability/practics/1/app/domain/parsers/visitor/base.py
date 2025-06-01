import ast
from typing import Protocol, Any, MutableMapping


class IASTVisitor(Protocol):
    def visit(self, node: ast.AST) -> Any: ...

    @property
    def current_line(self) -> int: ...

    @property
    def operators(self) -> MutableMapping[str, list[Any]]: ...

    @property
    def operands(self) -> MutableMapping[str, list[Any]]: ...

    @property
    def stats(self) -> MutableMapping[str, int]: ...

    @property
    def import_aliases(self) -> MutableMapping[str, str]: ...

    @property
    def global_vars(self) -> set[str]: ...
