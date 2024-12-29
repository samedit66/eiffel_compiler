from __future__ import annotations
from abc import ABC
from dataclasses import (
    dataclass,
    field,
)

from expressions import (
    Expression,
    FeatureCall,
    ResultConst,
    BracketAccess,
)


class Statement(ABC):
    pass


type StatementList = list[Statement]


@dataclass
class Assignment(Statement):
    location: Expression
    expr: Expression


@dataclass
class ElseifStmtBranch:
    condition: Expression
    stmt: StatementList


@dataclass
class IfStmt(Statement):
    condition: Expression
    then_stmt: StatementList
    elseif_stmts: list[ElseifStmtBranch] = field(default_factory=list)
    else_stmt: StatementList


@dataclass
class LoopStmt(Statement):
    init_stmts: StatementList
    until_cond: Expression
    body: StatementList


@dataclass
class WhenSection(Statement):
    pass


@dataclass
class InspectStmt(Statement):
    expr: Expression
    when_sections: list[WhenSection]
    else_section: StatementList = field(default_factory=list)


@dataclass
class StatementList:
    
    @classmethod
    def from_list(cls, statement_list: list) -> StatementList:
        return cls()
