from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from tree.expressions import (
    Expression,
    FeatureCall,
    UnknownNodeTypeError,
    )
from tree.base import is_empty_node


class Statement(ABC):
    
    @staticmethod
    def from_dict(stmt_dict: dict) -> Statement:
        node_type = stmt_dict["type"]
        match node_type:
            case "assign_stmt":
                return Assignment.from_dict(stmt_dict)
            case "if_stmt":
                return IfStmt.from_dict(stmt_dict)
            case "loop_stmt":
                return LoopStmt.from_dict(stmt_dict)
            case "inspect_stmt":
                return InspectStmt.from_dict(stmt_dict)
            case "feature_call":
                return RoutineCall.from_dict(stmt_dict)
            case "create_stmt":
                return CreateStmt.from_dict(stmt_dict)
            case _:
                raise UnknownNodeTypeError(f"Unknown statement type: {node_type}")
            

class StatementList:
    
    @staticmethod
    def from_list(stmts_list: list) -> list[Statement]:
        return [Statement.from_dict(stmt) for stmt in stmts_list if not is_empty_node(stmt)]


@dataclass(match_args=True)
class FieldName:
    name: str


@dataclass(match_args=True)
class Assignment(Statement):
    location: Expression
    value: Expression

    @classmethod
    def from_dict(cls, assignment_dict: dict) -> Assignment:
        location_node = assignment_dict["left"]
        if location_node["type"] == "ident_lit":
            location = FieldName(location_node["value"])
        else: # BracketAccess или Result
            location = Expression.from_dict(location_node)
        value = Expression.from_dict(assignment_dict["right"])
        return cls(location, value)


@dataclass(match_args=True)
class ElseifStmtBranch:
    condition: Expression
    body: StatementList

    @classmethod
    def from_dict(cls, elseif_stmt_dict: dict) -> ElseifStmtBranch:
        condition = Expression.from_dict(elseif_stmt_dict["cond"])
        body = StatementList.from_list(elseif_stmt_dict["body"])
        return cls(condition, body)


@dataclass(match_args=True)
class IfStmt(Statement):
    condition: Expression
    then_stmt: StatementList
    elseif_stmts: list[ElseifStmtBranch]
    else_stmt: StatementList

    @classmethod
    def from_dict(cls, if_stmt_dict: dict) -> IfStmt:
        condition = Expression.from_dict(if_stmt_dict["cond"])
        then_stmt = StatementList.from_list(if_stmt_dict["then_clause"])
        elseif_stmts = [
            ElseifStmtBranch.from_dict(elseif_stmt)
            for elseif_stmt in if_stmt_dict["elseif_clauses"]
            ]
        else_stmt = StatementList.from_list(if_stmt_dict["else_clause"])
        return cls(condition, then_stmt, elseif_stmts, else_stmt)


@dataclass(match_args=True)
class LoopStmt(Statement):
    init_stmts: StatementList
    until_cond: Expression
    body: StatementList

    @classmethod
    def from_dict(cls, loop_dict: dict) -> LoopStmt:
        init_stmts = StatementList.from_list(loop_dict["init"])
        until_cond = Expression.from_dict(loop_dict["cond"])
        body = StatementList.from_list(loop_dict["body"])
        return cls(init_stmts, until_cond, body)


class Choice(ABC):
    
    @staticmethod
    def from_dict(choice_dict: dict) -> Choice:
        choice_type = choice_dict["type"]
        if choice_type == "choice_interval":
            return IntervalChoice.from_dict(choice_dict)
        
        return ValueChoice(Expression.from_dict(choice_dict)) 


@dataclass(match_args=True)
class ValueChoice(Choice):
    value: Expression


@dataclass(match_args=True)
class IntervalChoice(Choice):
    start: Expression
    end: Expression

    @classmethod
    def from_dict(cls, interval_choice_dict: dict) -> IntervalChoice:
        start = Expression.from_dict(interval_choice_dict["start"])
        end = Expression.from_dict(interval_choice_dict["end"])
        return cls(start, end)


@dataclass(match_args=True)
class WhenSection(Statement):
    choices: list[Choice]
    body: StatementList

    @classmethod
    def from_dict(cls, when_section_dict: dict) -> WhenSection:
        choices = [Choice.from_dict(choice) for choice in when_section_dict["choices"]]
        body = StatementList.from_list(when_section_dict["body"])
        return cls(choices, body)
    
    
@dataclass(match_args=True)
class InspectStmt(Statement):
    expr: Expression
    when_sections: list[WhenSection]
    else_section: StatementList

    @classmethod
    def from_dict(cls, inspect_stmt_dict: dict) -> InspectStmt:
        expr = Expression.from_dict(inspect_stmt_dict["expr"])
        when_sections = [WhenSection.from_dict(when) for when in inspect_stmt_dict["when_clauses"]]
        else_section = StatementList.from_list(inspect_stmt_dict["else_clause"])
        return cls(expr, when_sections, else_section)


@dataclass(match_args=True)
class RoutineCall(Statement):
    feature_call: FeatureCall

    @classmethod
    def from_dict(cls, feature_call: dict) -> RoutineCall:
        feature_call = FeatureCall.from_dict(feature_call)
        return cls(feature_call)


@dataclass(match_args=True)
class CreateStmt(Statement):
    constructor_call: FeatureCall
    type_name: str | None

    @classmethod
    def from_dict(cls, create_stmt_dict: dict) -> CreateStmt:
        constructor_call = FeatureCall.from_dict(create_stmt_dict["constructor_call"])
        type_name = None if is_empty_node(create_stmt_dict["type_name"]) else create_stmt_dict["type_name"]
        return cls(type_name, constructor_call)
