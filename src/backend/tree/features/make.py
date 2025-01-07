from tree.features import *
from tree.type_decl import make_type_decl
from tree.expr import ResultConst, make_expr
from tree.stmts import Assignment, make_stmt


def make_feature_list(feature_clauses: list) -> list[Feature]:
    features = []

    for feature_clause in feature_clauses:
        clients = feature_clause["clients"]

        for feature_dict in feature_clause["feature_list"]:
            feature_dicts = separate_declarations(feature_dict)

            for feature_dict in feature_dicts:
                match feature_dict["type"]:
                    case "class_field":
                        features.append(make_field(clients, feature_dict))
                    case "class_constant":
                        features.append(make_constant(clients, feature_dict))
                    case "class_routine":
                        features.append(make_method(clients, feature_dict))
                    case unknown_feature_type:
                        raise UnknownNodeTypeError(f"Unknown feature node type: {unknown_feature_type}")

    return features


def make_field(clients: list[Identifier], field_dict: dict) -> Field:
    return Field(
        location=Location.from_dict(field_dict["location"]),
        name=field_dict["name_and_type"]["name"],
        clients=clients,
        value_type=make_type_decl(field_dict["name_and_type"]["field_type"]),
        )


def make_constant(clients: list[Identifier], constant_dict: dict) -> Constant:
    return Constant(
        location=Location.from_dict(constant_dict["location"]),
        name=constant_dict["name_and_type"]["name"],
        clients=clients,
        value_type=make_type_decl(constant_dict["name_and_type"]["field_type"]),
        constant_value=make_expr(constant_dict["constant_value"]),
        )


def make_parameters(parameters_list: list) -> list[Parameter]:
    parameters = []

    for parameter_dict in parameters_list:
        parameter_dicts = separate_declarations(parameter_dict)

        parameters.extend(
            Parameter(
                location=Location.from_dict(parameter_dict["location"]),
                name=parameter_dict["name_and_type"]["name"],
                parameter_type=make_type_decl(parameter_dict["name_and_type"]["field_type"]),
            )
            for parameter_dict in parameter_dicts
        )

    return parameters


def make_local_var_decls(var_decl_list: list) -> list[LocalVarDecl]:
    var_decls = []

    for var_decl_dict in var_decl_list:
        var_decls_dicts = separate_declarations(var_decl_dict)

        var_decls.extend(
            LocalVarDecl(
                location=Location.from_dict(var_decl_dict["location"]),
                name=var_decl_dict["name_and_type"]["name"],
                value_type=make_type_decl(var_decl_dict["name_and_type"]["field_type"]),
            )
            for var_decl_dict in var_decls_dicts
        )

    return var_decls


def make_conditions(condition_list: list) -> list[Condition]:
    conditions = []

    for condition_dict in condition_list:
        condition = Condition(
            location=Location.from_dict(condition_dict["location"]),
            condition_expr=make_expr(condition_dict["cond"]),
            tag=condition_dict["tag"] if "tag" in condition_dict else None,
        )
        conditions.append(condition)

    return conditions


def make_do(method_dict: dict) -> list[Statement]:
    body = method_dict["body"]
    stmts = [make_stmt(stmt_dict) for stmt_dict in body["do"]]

    then = body["then"]
    if not is_empty_node(then):
        stmts.append(
            Assignment(
                location=Location.from_dict(then["location"]),
                target=ResultConst(),
                value=make_expr(then)
            )
        )

    return stmts


def make_method(clients: list[Identifier], method_dict: dict) -> Method:
    return Method(
        location=Location.from_dict(method_dict["location"]),
        name=method_dict["name_and_type"]["name"],
        clients=clients,
        is_deferred=method_dict["body"]["is_deferred"],
        return_type=make_type_decl(method_dict["name_and_type"]["field_type"]),
        parameters=make_parameters(method_dict["params"]),
        do=make_do(method_dict),
        local_var_decls=make_local_var_decls(method_dict["body"]["local"]),
        require=make_conditions(method_dict["body"]["require"]),
        ensure=make_conditions(method_dict["body"]["ensure"]),
    )


def separate_declarations(decl_node_dict: dict) -> list:
    """Используется для разделения деклараций полей, методов, констант
    и параметров, объявленных "вместе":
    Необходимо объявления вида
            a, b: INTEGER;
    перевести в
            a: INTEGER; b: INTEGER;
    
    Недостаток данного разделения заключается в том, что частично
    теряется информация о месте объявления - сохраняются только номера строк

    :param decl_node_dict: Узел объявления
    :return: Преобразованный, "разделенный", список узлов, также в виде словарей
    """
    separated = []

    node_type = decl_node_dict["type"]
    location = decl_node_dict["location"]

    name_and_type = decl_node_dict["name_and_type"]

    names = name_and_type["names"]
    for name in names:
        name_and_type_ = {
            "field_type": name_and_type["field_type"],
            "name": name
        }
        decl_node_dict_ = {
            **decl_node_dict,
            "type": node_type,
            "location": location,
            "name_and_type": name_and_type_
            }
            
        separated.append(decl_node_dict_)

    return separated
