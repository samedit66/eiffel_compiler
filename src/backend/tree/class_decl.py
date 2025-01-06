from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

from tree.base import *
from tree.features import FeatureList, Feature
from tree.type_decl import GenericType, TypeDecl


@dataclass(match_args=True)
class Alias:
    original_name: str
    alias_name: str

    @classmethod
    def from_dict(cls, alias_dict: dict) -> Alias:
        return cls(alias_dict["original_name"], alias_dict["alias_name"])


@dataclass(match_args=True)
class RenameSection:
    aliases: list[Alias]

    @classmethod
    def from_list(cls, aliases_list: list) -> RenameSection:
        aliases = [Alias.from_dict(alias) for alias in aliases_list]
        return cls(aliases)


@dataclass(match_args=True)
class UndefineSection:
    features: IdentifierList


@dataclass(match_args=True)
class RedefineSection:
    features: IdentifierList


@dataclass(match_args=True)
class SelectSection:
    features: IdentifierList


@dataclass(match_args=True)
class GenericList:
    generics: list[GenericType] = field(default_factory=list)

    @classmethod
    def from_list(cls, generics_list: list) -> GenericList:
        generics = [
            GenericType(generic_type["generic_type"]["type_name"])
            if generic_type["type"] == "generic"
            else GenericType(
                generic_type["generic_type"]["type_name"],
                TypeDecl.from_dict(generic_type["generic_type"]["parent"])
                )
            for generic_type in generics_list
        ]
        return cls(generics)


@dataclass(match_args=True)
class Inheritance:
    class_name: str
    generic_list: GenericList
    rename_section: RenameSection
    undefine_section: UndefineSection
    redefine_section: RedefineSection
    select_section: SelectSection

    @classmethod
    def from_dict(cls, inherit_clause: dict) -> Inheritance:
        class_name = inherit_clause["parent_header"]
        generic_list = GenericList.from_list(inherit_clause["parent_header"]["generics"])
        rename_section = RenameSection.from_list(inherit_clause["rename_clause"])
        undefine_section = UndefineSection(inherit_clause["undefine_clause"])
        redefine_section = RedefineSection(inherit_clause["redefine_clause"])
        select_section = SelectSection(inherit_clause["select_clause"])
        return cls(class_name, generic_list, rename_section, undefine_section, redefine_section, select_section)


@dataclass(match_args=True)
class InheritSection:
    ancestors: list[Inheritance]

    @classmethod
    def from_list(cls, inherit_section: list) -> InheritSection:
        ancestors = [Inheritance.from_dict(ancestor) for ancestor in inherit_section]
        return cls(ancestors)


@dataclass(match_args=True)
class CreateSection:
    constructors: IdentifierList

    @classmethod
    def from_list(cls, constructors: IdentifierList) -> CreateSection:
        return cls(constructors)


@dataclass(match_args=True)
class FeatureSection:
    feature_list: list[FeatureList]

    @classmethod
    def from_list(cls, features: list) -> FeatureSection:
        feature_list = [
            FeatureList.from_list(feature_clause)
            for feature_clause in features
        ]
        return cls(feature_list)
    

@dataclass(match_args=True)
class ClassDecl(Node):
    name: str
    is_deferred: bool
    generic_list: GenericList = field(default_factory=GenericList)
    inherit_section: InheritSection | None = None
    create_section: CreateSection | None = None
    feature_section: FeatureSection | None = None
    file_path: Path | None = None

    @classmethod
    def from_dict(cls, class_decl: dict) -> ClassDecl:
        location = Location.from_dict(class_decl["location"])
        name = class_decl["header"]["name"]
        is_deferred = class_decl["header"]["is_deferred"]
        generic_list = GenericList.from_list(class_decl["header"]["generics"])
        inherit_section = InheritSection.from_list(class_decl["inheritance"])
        create_section = CreateSection.from_list(class_decl["creators"])
        feature_section = FeatureSection.from_list(class_decl["features"])
        file_path = Path(class_decl["file_path"]) if class_decl["file_path"] != "stdin" else None
        return cls(
            location,
            name,
            is_deferred,
            generic_list,
            inherit_section,
            create_section,
            feature_section,
            file_path,
            )
    