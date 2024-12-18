from testlib import use, expect, run_eiffel


@expect(
    {
        "classes": [
            {
                "type": "class_decl",
                "header": {
                    "name": "EMPTY",
                    "generics": []
                },
                "inheritance": [],
                "creators": [],
                "features": []
            }
        ]
    },
    full_match=True,
)
@run_eiffel
@use("EmptyClass.e")
def test_empty_class():
    pass


@expect(
    {
        "type": "loop_stmt",
        "init": [
            {
                "type": "assign_stmt",
                "left": {
                    "type": "ident_lit",
                    "value": "i"
                },
                "right": {
                    "type": "int_const",
                    "value": 1
                }
            }
        ],
        "cond": {
            "type": "eq_op",
            "left": {
                "type": "feature_call",
                "owner": {
                    "type": "empty"
                },
                "feature": {
                    "name": "i",
                    "args_list": []
                }
            },
            "right": {
                "type": "feature_call",
                "owner": {
                    "type": "empty"
                },
                "feature": {
                    "name": "mm",
                    "args_list": []
                }
            }
        },
        "body": [
            {
                "type": "assign_stmt",
                "left": {
                    "type": "result_const"
                },
                "right": {
                    "type": "add_op",
                    "left": {
                        "type": "result_const"
                    },
                    "right": {
                        "type": "bracket_access",
                        "source": {
                            "type": "feature_call",
                            "owner": {
                                "type": "empty"
                            },
                            "feature": {
                                "name": "months",
                                "args_list": []
                            }
                        },
                        "index": {
                            "type": "feature_call",
                            "owner": {
                                "type": "empty"
                            },
                            "feature": {
                                "name": "i",
                                "args_list": []
                            }
                        }
                    }
                }
            }
        ]
    }
)
@run_eiffel
@use("Loop.e")
def test_loop():
    pass


@expect(
    {
        "classes": [
            {
                "type": "class_decl",
                "header": {
                    "name": "RECTANGLE",
                    "generics": []
                },
                "inheritance": [
                    {
                        "type": "parent",
                        "parent_header": {
                            "name": "POLYGON",
                            "generics": []
                        },
                        "rename_clause": [],
                        "undefine_clause": [],
                        "redefine_clause": [
                            "perimeter"
                        ],
                        "select_clause": []
                    }
                ],
                "creators": [],
                "features": []
            }
        ]
    },
    full_match=True,
)
@run_eiffel
@use("SingleInheritance.e")
def test_single_inheritance():
    pass


@expect(
    {
        "classes": [
            {
                "type": "class_decl",
                "header": {
                    "name": "LINKED_QUEUE",
                    "generics": []
                },
                "inheritance": [
                    {
                        "type": "parent",
                        "parent_header": {
                            "name": "QUEUE",
                            "generics": []
                        },
                        "rename_clause": [],
                        "undefine_clause": [
                            "is_empty",
                            "copy",
                            "is_equal"
                        ],
                        "redefine_clause": [
                            "linear_representation",
                            "prune_all",
                            "extend"
                        ],
                        "select_clause": [
                            "item",
                            "put"
                        ]
                    },
                    {
                        "type": "parent",
                        "parent_header": {
                            "name": "LINKED_LIST",
                            "generics": []
                        },
                        "rename_clause": [
                            {
                                "type": "alias",
                                "original_name": "item",
                                "alias_name": "ll_item"
                            },
                            {
                                "type": "alias",
                                "original_name": "remove",
                                "alias_name": "ll_remove"
                            },
                            {
                                "type": "alias",
                                "original_name": "make",
                                "alias_name": "ll_make"
                            },
                            {
                                "type": "alias",
                                "original_name": "remove_left",
                                "alias_name": "remove"
                            },
                            {
                                "type": "alias",
                                "original_name": "put",
                                "alias_name": "ll_put"
                            }
                        ],
                        "undefine_clause": [
                            "fill",
                            "append",
                            "prune",
                            "readable",
                            "writable",
                            "prune_all",
                            "extend",
                            "force",
                            "is_inserted"
                        ],
                        "redefine_clause": [
                            "duplicate",
                            "linear_representation"
                        ],
                        "select_clause": [
                            "remove"
                        ]
                    }
                ],
                "creators": [],
                "features": []
            }
        ]
    }
)
@run_eiffel
@use("MultipleInheritance.e")
def test_multiple_inheritance():
    pass
