from __future__ import annotations
from dataclasses import (
    dataclass,
    field,
    )


@dataclass
class Alias:
    original_name: str
    alias_name: str


@dataclass
class RenameSection:
    aliases: list[Alias] = field(default_factory=list)


@dataclass
class UndefineSection:
    features: list[str] = field(default_factory=list)


@dataclass
class RedefineSection:
    features: list[str] = field(default_factory=list)


@dataclass
class SelectSection:
    features: list[str] = field(default_factory=list)


@dataclass
class Inheritance:
    class_name: str
    # generics: list
    rename_section: RenameSection
    undefine_section: UndefineSection
    redefine_section: RedefineSection
    select_section: SelectSection


@dataclass
class InheritSection:
    parents: list[Inheritance] = field(default_factory=list)

    @classmethod
    def from_list(cls, inherit_section: list) -> InheritSection:
        parents = [Inheritance.from_dict(parent) for parent in inherit_section]
        return cls(parents)


@dataclass
class CreateSection:
    constructors: list[str] = field(default_factory=list)

    @classmethod
    def from_list(cls, constructors: list[str]) -> CreateSection:
        return cls(constructors)


@dataclass
class ClassDecl:
    name: str
    inherit_section: InheritSection
    create_section: CreateSection

    @classmethod
    def from_dict(cls, class_decl: dict) -> ClassDecl:
        name = class_decl["header"]["name"]
        inherit_section = InheritSection.from_list(class_decl["inheritance"])
        create_section = CreateSection.from_list(class_decl["creators"])
        return cls(name, inherit_section, create_section)


node = {
    "type": "class_decl",
    "header": {
        "name": "EMPTY",
        "generics": []
    },
    "inheritance": [],
    "creators": [],
    "features": []
}

class_decl = ClassDecl.from_dict(node)
print(class_decl)
