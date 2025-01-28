from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

from ...tree.class_decl import ClassDecl, GenericSpec
from ...tree.base import Location


from .inheritance import FTable, analyze_inheritance


@dataclass(kw_only=True)
class FlattenClass:
    name: str
    is_deferred: bool
    generics: list[GenericSpec]
    features: FTable
    source_file: Path | None
    location: Location
    parents: list[FlattenClass]
    constructors: list[str]

    def __hash__(self) -> int:
        return hash(self.name)
    
    @classmethod
    def from_class_decl(cls, decl: ClassDecl) -> FlattenClass:
        return cls(
            name=decl.class_name,
            is_deferred=decl.is_deferred,
            generics=decl.generics,
            features=analyze_inheritance(decl),
            source_file=decl.defined_in_file,
            location=decl.location,
            parents=[
                FlattenClass.from_class_decl(parent.class_decl)
                for parent in decl.inherit
            ],
            constructors=decl.create,
        )


def process_stage1(classes: set[ClassDecl]) -> list[FlattenClass]:
    exps = []

    flatten_classes = []
    for decl in classes:
        try:
            flatten_classes.append(FlattenClass.from_class_decl(decl))
        except Exception as e:
            exps.append(e)

    if exps:
        raise ExceptionGroup("Semantic problems at stage 1", exps)

    return flatten_classes
