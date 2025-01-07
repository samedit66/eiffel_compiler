from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from tree.base import *
from tree.expr import Expr, FeatureCall


class Statement(Node, ABC): pass


@dataclass(match_args=True, kw_only=True)
class Assignment(Statement):
    target: Identifier | Expr
    value: Expr


@dataclass(match_args=True, kw_only=True)
class ElseifBranch(Statement):
    condition: Expr
    body: list[Statement]


@dataclass(match_args=True, kw_only=True)
class IfStmt(Statement):
    condition: Expr
    then_branch: list[Statement]
    elseif_branches: list[ElseifBranch]
    else_branch: list[Statement]


@dataclass(match_args=True, kw_only=True)
class LoopStmt(Statement):
    init_stmts: list[Statement]
    until_cond: Expr
    body: list[Statement]


class Choice(ABC): pass


@dataclass(match_args=True, kw_only=True)
class ValueChoice(Choice):
    value: Expr


@dataclass(match_args=True, kw_only=True)
class IntervalChoice(Choice):
    start: Expr
    end: Expr


@dataclass(match_args=True, kw_only=True)
class WhenBranch(Statement):
    choices: list[Choice]
    body: list[Statement]

    
@dataclass(match_args=True, kw_only=True)
class InspectStmt(Statement):
    expr: Expr
    when_branches: list[WhenBranch]
    else_branch: list[Statement]


@dataclass(match_args=True, kw_only=True)
class RoutineCall(Statement):
    feature_call: FeatureCall
