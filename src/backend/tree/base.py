type IdentifierList = list[str]


def is_empty_node(node_dict: dict) -> bool:
    return node_dict["type"] == "empty"
