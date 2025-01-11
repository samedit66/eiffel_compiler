from __future__ import annotations

from tree.base import *
from tree.class_decl.types import *
from tree.features import make_feature_list


def make_class_decl(class_decl_dict: dict) -> ClassDecl:
    return ClassDecl(
        location=Location.from_dict(class_decl_dict["location"]),
        class_name=class_decl_dict["header"]["name"],
        is_deferred=class_decl_dict["header"]["is_deferred"],
        generics=[
            make_generic(generic_dict) for generic_dict in class_decl_dict["header"]["generics"]
        ],
        inherit=[
            Parent(
                location=Location.from_dict(parent_dict["location"]),
                class_name=parent_dict["parent_header"]["name"],
                generics=[
                    make_generic(generic_dict) for generic_dict in parent_dict["parent_header"]["generics"]
                ],
                rename=[
                    Alias(
                        location=Location.from_dict(pair_dict["location"]),
                        original_name=pair_dict["original_name"],
                        alias_name=pair_dict["alias_name"],
                    )
                    for pair_dict in parent_dict["rename_clause"]
                ],
                undefine=parent_dict["undefine_clause"],
                redefine=parent_dict["redefine_clause"],
                select=parent_dict["select_clause"],
            )
            for parent_dict in class_decl_dict["inheritance"]
        ],
        create=class_decl_dict["creators"],
        features=make_feature_list(class_decl_dict["features"]),
        defined_in_file=class_decl_dict["file_path"],
    )


def make_generic(generic_dict: dict) -> GenericType:
    return GenericType(
        location=Location.from_dict(generic_dict["location"]),
        template_type_name=generic_dict["generic_type"]["type_name"],
        required_parent=generic_dict["parent"],
    )
