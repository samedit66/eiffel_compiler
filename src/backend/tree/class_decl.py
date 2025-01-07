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

type RenameSection = list[Alias]


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


@dataclass(match_args=True, kw_only=True)
class Ancestor:
    class_name: str
    generic_list: GenericList
    rename_section: RenameSection
    undefine_section: UndefineSection
    redefine_section: RedefineSection
    select_section: SelectSection

    @classmethod
    def from_dict(cls, ancestor_dict: dict) -> Ancestor:
        class_name = ancestor_dict["parent_header"]["name"]
        generic_list = GenericList.from_list(ancestor_dict["parent_header"]["generics"])
        rename_section = RenameSection.from_list(ancestor_dict["rename_clause"])
        undefine_section = UndefineSection(ancestor_dict["undefine_clause"])
        redefine_section = RedefineSection(ancestor_dict["redefine_clause"])
        select_section = SelectSection(ancestor_dict["select_clause"])
        return cls(
            class_name=class_name,
            generic_list=generic_list,
            rename_section=rename_section,
            undefine_section=undefine_section,
            redefine_section=redefine_section,
            select_section=select_section,
            )

type InheritSection = list[Ancestor]


type Constructor = Identifier
type CreateSection = list[Constructor]


type FeatureSection = list[Feature]

def make_feature_section(feature_clauses: list) -> FeatureSection:
    features = []

    for feature_clause in feature_clauses:
        clients = feature_clause["clients"]
        

    return features


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
    inherit_section: InheritSection
    create_section: CreateSection
    feature_section: FeatureSection
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
    