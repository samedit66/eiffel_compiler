from __future__ import annotations
from dataclasses import (
    dataclass,
    field,
    )

from base import IdentifierList
from features import FeatureList
from type_decl import GenericType, ConcreteType


@dataclass
class Alias:
    original_name: str
    alias_name: str

    @classmethod
    def from_dict(cls, alias_dict: dict) -> Alias:
        return cls(alias_dict["original_name"], alias_dict["alias_name"])


@dataclass
class RenameSection:
    aliases: list[Alias] = field(default_factory=list)

    @classmethod
    def from_list(cls, aliases_list: list) -> RenameSection:
        aliases = [Alias.from_dict(alias) for alias in aliases_list]
        return cls(aliases)


@dataclass
class UndefineSection:
    features: IdentifierList = field(default_factory=list)


@dataclass
class RedefineSection:
    features: IdentifierList = field(default_factory=list)


@dataclass
class SelectSection:
    features: IdentifierList = field(default_factory=list)


@dataclass
class GenericList:
    generics: list[GenericType] = field(default_factory=list)

    @classmethod
    def from_list(cls, generics_list: list) -> GenericList:
        generics = [
            GenericType(generic_type["type_name"])
            if generic_type["type"] == "generic"
            else GenericType(generic_type["type_name"], ConcreteType.from_dict(generic_type["parent"]))
            for generic_type in generics_list
        ]
        return cls(generics)


@dataclass
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


@dataclass
class InheritSection:
    ancestors: list[Inheritance] = field(default_factory=list)

    @classmethod
    def from_list(cls, inherit_section: list) -> InheritSection:
        ancestors = [Inheritance.from_dict(ancestor) for ancestor in inherit_section]
        return cls(ancestors)


@dataclass
class CreateSection:
    constructors: IdentifierList = field(default_factory=list)

    @classmethod
    def from_list(cls, constructors: IdentifierList) -> CreateSection:
        return cls(constructors)


@dataclass
class FeatureSection:
    feature_list: FeatureList

    @classmethod
    def from_list(cls, features: list) -> FeatureSection:
        feature_list = [
            FeatureList.from_list(feature_clause)
            for feature_clause in features
        ]
        return cls(feature_list)
    

@dataclass
class ClassDecl:
    name: str
    generic_list: GenericList
    inherit_section: InheritSection
    create_section: CreateSection
    feature_section: FeatureSection

    @classmethod
    def from_dict(cls, class_decl: dict) -> ClassDecl:
        name = class_decl["header"]["name"]
        generic_list = GenericList.from_list(class_decl["header"]["generics"])
        inherit_section = InheritSection.from_list(class_decl["inheritance"])
        create_section = CreateSection.from_list(class_decl["creators"])
        feature_section = FeatureSection.from_list(class_decl["features"])
        return cls(name, generic_list, inherit_section, create_section, feature_section)
