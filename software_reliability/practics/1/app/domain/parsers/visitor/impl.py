import ast
from collections import defaultdict
from copy import deepcopy, copy
from typing import Any, Union, MutableMapping, Final, override


class ParentSetter(ast.NodeVisitor):
    def __init__(self) -> None:
        self._parent: ast.AST | None = None

    @override
    def visit(self, node: ast.AST) -> None:
        node.parent = self._parent
        prev_parent: ast.AST = self._parent
        self._parent = node
        super().visit(node)
        self._parent = prev_parent


class BaseAnalyzer(ast.NodeVisitor):
    def __init__(self) -> None:
        self._operators: Final[MutableMapping[str, list[Any]]] = defaultdict(list)
        self._operands: Final[MutableMapping[str, list[Any]]] = defaultdict(list)
        self._stats: Final[MutableMapping[str, int]] = defaultdict(int)
        self._current_line: int = 0
        self._import_aliases: Final[MutableMapping[str, str]] = {}
        self._global_vars: Final[set[str]] = set()
        self._parent_setter: Final[ParentSetter] = ParentSetter()

    @override
    def visit(self, node: ast.AST) -> Any:
        self._parent_setter.visit(node)
        self._current_line: int = getattr(node, 'lineno', self._current_line)
        method: str = 'visit_' + node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node)  # type: ignore

    def get_full_name(self, node: Union[ast.Name, ast.Attribute, ast.expr]) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self.get_full_name(node.value)}.{node.attr}"
        return ""

    @property
    def operators(self) -> MutableMapping[str, list[Any]]:
        result: MutableMapping[str, list[Any]] = deepcopy(self._operators)
        return result

    @property
    def operands(self) -> MutableMapping[str, list[Any]]:
        result: MutableMapping[str, list[Any]] = deepcopy(self._operands)
        return result

    @property
    def stats(self) -> MutableMapping[str, int]:
        result: MutableMapping[str, int] = copy(self._stats)
        return result

    @property
    def import_aliases(self) -> MutableMapping[str, str]:
        result: MutableMapping[str, str] = copy(self._import_aliases)
        return result

    @property
    def global_vars(self) -> set[str]:
        result: set[str] = copy(self._global_vars)
        return result

    @property
    def current_line(self) -> int:
        return self._current_line

    @staticmethod
    def _is_type_annotation(node: ast.Name) -> bool:
        parent = getattr(node, 'parent', None)
        if isinstance(parent, (ast.AnnAssign, ast.Assign)):
            if hasattr(parent, 'annotation') or any(
                    hasattr(target, 'annotation') for target in getattr(parent, 'targets', [])
            ):
                return True
        if isinstance(parent, ast.Subscript):
            return True
        return False
