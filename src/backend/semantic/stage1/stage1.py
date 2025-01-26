from __future__ import annotations
from dataclasses import dataclass

from ...tree.class_decl import ClassDecl

from .featureset import FeatureSet
from .inheritance import analyze_inheritance


@dataclass(match_args=True, kw_only=True)
class FlattenClass:
    decl: ClassDecl
    own_features: FeatureSet
    parents: list[FlattenClass]

    @property
    def name(self) -> str:
        return self.decl.class_name
    
    @property
    def source_file(self) -> str:
        return self.decl.defined_in_file
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    @classmethod
    def from_class_decl(cls, decl: ClassDecl) -> FlattenClass:
        return cls(
            decl=decl,
            own_features=analyze_inheritance(decl),
            parents=[
                FlattenClass.from_class_decl(parent.class_decl)
                for parent in decl.inherit
            ]
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
