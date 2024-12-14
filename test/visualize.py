from pathlib import Path
import json
import sys

from graphviz import Digraph

from testlib.utils import run_eiffel_parser


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


def visualize(eiffel_file: str | Path, filename: str | Path = "dot-output/graph.gv") -> None:
    program_text = Path(eiffel_file).read_text()
    stdout, stderr = run_eiffel_parser(program_text)
    tree = json.loads(stdout)
    graph = dict_to_dot(tree)
    graph.view(filename)


if __name__ == "__main__":
    files = sys.argv[1:]

    if not files:
        print("Expected at least one eiffel file")
        sys.exit(1)
    
    visualize(files[0])
