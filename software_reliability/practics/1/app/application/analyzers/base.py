import ast
from typing import Protocol

from app.domain.parsers.assigment.base import IAssignmentHandler
from app.domain.parsers.visitor.base import IASTVisitor


class IAnalyzerComponent(
    IASTVisitor,
    # IOperatorContainer,
    # IOperandContainer,
    # IStatsContainer,
    # IImportAliasContainer,
    # IGlobalVarContainer,
    # ILineTracker,
    IAssignmentHandler,
    Protocol
):
    def get_full_name(self, node: ast.Name | ast.Attribute) -> str: ...
