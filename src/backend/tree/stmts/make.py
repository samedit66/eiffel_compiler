from __future__ import annotations

from tree.base import *
from tree.stmts.types import *


def make_stmt(stmt_dict: dict) -> Statement:
    match stmt_dict["type"]:
        case "assign_stmt":
            return make_assignment_stmt(stmt_dict);
        case "if_stmt":
            return IfStmt.from_dict(stmt_dict)
        case "loop_stmt":
            return LoopStmt.from_dict(stmt_dict)
        case "inspect_stmt":
            return InspectStmt.from_dict(stmt_dict)
        case "feature_call":
            return RoutineCall.from_dict(stmt_dict)
        case "create_stmt":
            return make_create_stmt(stmt_dict)
        case unknown_node_type:
            raise UnknownNodeTypeError(f"Unknown statement type: {unknown_node_type}")


@dataclass(match_args=True)
class CreateStmt(Statement):
    constructor_call: FeatureCall
    type_name: str | None

    @classmethod
    def from_dict(cls, create_stmt_dict: dict) -> CreateStmt:
        location = Location.from_dict(create_stmt_dict["location"])
        constructor_call = FeatureCall.from_dict(create_stmt_dict["constructor_call"])
        type_name = None if is_empty_node(create_stmt_dict["type_name"]) else create_stmt_dict["type_name"]
        return cls(location, constructor_call, type_name)


def make_create_stmt(create_stmt_dict: dict) -> Assignment:
    owner = create_stmt_dict["constructor_call"]["owner"]

    return Assignment(
        location=Location.from_dict(create_stmt_dict["location"]),
        target=
    )

def make_assignment_stmt(assignment_stmt_dict: dict) -> Assignment:
    left = assignment_stmt_dict["left"]
    return Assignment(
        location=Location.from_dict(assignment_stmt_dict["location"]),
        target=left["value"] if left["type"] == "ident_lit" else make_expr(left),
        value=make_expr(assignment_stmt_dict["right"]),
    )


@dataclass(match_args=True)
class ElseifStmtBranch(Statement):
    condition: Expression
    body: StatementList

    @classmethod
    def from_dict(cls, elseif_stmt_dict: dict) -> ElseifStmtBranch:
        location = Location.from_dict(elseif_stmt_dict["location"])
        condition = Expression.from_dict(elseif_stmt_dict["cond"])
        body = StatementList.from_list(elseif_stmt_dict["body"])
        return cls(location, condition, body)


@dataclass(match_args=True)
class IfStmt(Statement):
    condition: Expression
    then_stmt: StatementList
    elseif_stmts: list[ElseifStmtBranch]
    else_stmt: StatementList

    @classmethod
    def from_dict(cls, if_stmt_dict: dict) -> IfStmt:
        location = Location.from_dict(if_stmt_dict["location"])
        condition = Expression.from_dict(if_stmt_dict["cond"])
        then_stmt = StatementList.from_list(if_stmt_dict["then_clause"])
        elseif_stmts = [
            ElseifStmtBranch.from_dict(elseif_stmt)
            for elseif_stmt in if_stmt_dict["elseif_clauses"]
            ]
        else_stmt = StatementList.from_list(if_stmt_dict["else_clause"])
        return cls(location, condition, then_stmt, elseif_stmts, else_stmt)


@dataclass(match_args=True)
class LoopStmt(Statement):
    init_stmts: StatementList
    until_cond: Expression
    body: StatementList

    @classmethod
    def from_dict(cls, loop_dict: dict) -> LoopStmt:
        location = Location.from_dict(loop_dict["location"])
        init_stmts = StatementList.from_list(loop_dict["init"])
        until_cond = Expression.from_dict(loop_dict["cond"])
        body = StatementList.from_list(loop_dict["body"])
        return cls(location, init_stmts, until_cond, body)


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
        location = Location.from_dict(when_section_dict["location"])
        choices = [Choice.from_dict(choice) for choice in when_section_dict["choices"]]
        body = StatementList.from_list(when_section_dict["body"])
        return cls(location, choices, body)
    
    
@dataclass(match_args=True)
class InspectStmt(Statement):
    expr: Expression
    when_sections: list[WhenSection]
    else_section: StatementList

    @classmethod
    def from_dict(cls, inspect_stmt_dict: dict) -> InspectStmt:
        location = Location.from_dict(inspect_stmt_dict["location"])
        expr = Expression.from_dict(inspect_stmt_dict["expr"])
        when_sections = [WhenSection.from_dict(when) for when in inspect_stmt_dict["when_clauses"]]
        else_section = StatementList.from_list(inspect_stmt_dict["else_clause"])
        return cls(location, expr, when_sections, else_section)


@dataclass(match_args=True)
class RoutineCall(Statement):
    feature_call: FeatureCall

    @classmethod
    def from_dict(cls, feature_call_dict: dict) -> RoutineCall:
        location = Location.from_dict(feature_call_dict["location"])
        feature_call = FeatureCall.from_dict(feature_call_dict)
        return cls(location, feature_call)


@dataclass(match_args=True)
class CreateStmt(Statement):
    constructor_call: FeatureCall
    type_name: str | None

    @classmethod
    def from_dict(cls, create_stmt_dict: dict) -> CreateStmt:
        location = Location.from_dict(create_stmt_dict["location"])
        constructor_call = FeatureCall.from_dict(create_stmt_dict["constructor_call"])
        type_name = None if is_empty_node(create_stmt_dict["type_name"]) else create_stmt_dict["type_name"]
        return cls(location, constructor_call, type_name)
