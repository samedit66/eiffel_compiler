import json
import subprocess
import pprint

from graphviz import Digraph


def run_eiffel_parser(
        eiffel_text: str,
        parser_name: str = "eiffelp",
        ) -> tuple[str, str]:
    """Возвращает результат работы парсера Eiffel по заданному файлу

    :param eiffel_text: текст программы на Eiffel
    :param parser_name: имя парсера

    :return: кортеж из двух строк: stdout и stderr
    """
    try:
        output = subprocess.run(
            [parser_name],
            input=eiffel_text.encode(),
            capture_output=True,
            )
    except FileNotFoundError:
        raise RuntimeError(f'Couldn\'t find eiffel parser by name "{parser_name}"')
    return (output.stdout.decode(), output.stderr.decode())


def _dict_node_to_dot(value, current_node, graph):
    if isinstance(value, dict):
        dict_to_dot(value, current_node, graph)
    elif isinstance(value, list):
        for i, leaf in enumerate(value):
            leaf_node = f"{current_node}.{i}"  
            graph.node(leaf_node, label=f"[{i}]") 
            graph.edge(current_node, leaf_node)  
            _dict_node_to_dot(leaf, leaf_node, graph)  
    else:
        leaf_node = f"{current_node}.{value}"
        graph.node(leaf_node, label=str(value))
        graph.edge(current_node, leaf_node)


def dict_to_dot(source: dict, parent=None, graph=None):
    if graph is None:
        graph = Digraph()
    
    for key, value in source.items():
        current_node = f"{parent}.{key}" if parent else key
        graph.node(current_node, label=key)

        if parent is not None:
            graph.edge(parent, current_node)

        _dict_node_to_dot(value, current_node, graph)

    return graph


def generate_dot(parser_output: str) -> None:
    tree = json.loads(parser_output)
    print(tree)


with open("test.e") as test_program:
    program_text = test_program.read()
    parser_output, _ = run_eiffel_parser(program_text)
    tree = json.loads(parser_output)
    dot = dict_to_dot(tree)
    dot.render('dot-output/round-table.gv', view=True)
