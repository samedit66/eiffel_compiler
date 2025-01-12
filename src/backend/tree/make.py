from tree.class_decl import *


def make_ast(ast_dict: dict) -> list[ClassDecl]:
    return [
        make_class_decl(class_decl_dict)
        for class_decl_dict in ast_dict["classes"]
    ]
