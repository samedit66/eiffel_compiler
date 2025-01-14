from collections import defaultdict
from typing import Iterable
from itertools import groupby

from ..tree.class_decl import ClassDecl, Parent

from .base import SemanticError


class DuplicatesError(SemanticError):
    """Ошибка, возникающая в ходе обнаружения классов-дубликатов
    найденных в системе, либо в секции наследования
    """

    def __init__(self, dups: Iterable[ClassDecl]) -> None:
        super().__init__(DuplicatesError.message(dups))
        self.dups = dups

    @staticmethod
    def message(dups: Iterable[ClassDecl]) -> str:
        msg_parts = [f"Found duplicated classes:"]

        for _, group in groupby(dups, key=lambda decl: decl.class_name):
            for dup in sorted(group, key=lambda decl: decl.location.first_line):
                msg_parts.append(
                    f"    {dup.class_name} in file {dup.defined_in_file}, line {dup.location.first_line}"
                    )

        return "\n".join(msg_parts)


class ParentDoesNotExistError(SemanticError):
    """Ошибка, возникающая, если класс наследуется от неизвестного родителя"""

    def __init__(self, nonexistent: dict[ClassDecl, list[Parent]]) -> None:
        super().__init__(ParentDoesNotExistError.message(nonexistent))
        self.nonexistent = nonexistent

    @staticmethod
    def message(nonexistent: dict[ClassDecl, list[Parent]]) -> str:
        msg_parts = [f"Found nonexistent parents:"]

        for decl in sorted(nonexistent, key=lambda decl: decl.class_name):
            msg_parts.append(f"For class {decl.class_name} in file {decl.defined_in_file}:")

            for parent in nonexistent[decl]:
                msg_parts.append(f"    Parent {parent.class_name}, line {parent.location.first_line}")

        return "\n".join(msg_parts)


def analyze_duplicates(classes: list[ClassDecl]) -> tuple[set[ClassDecl], set[ClassDecl]]:
    """Определяет множество классов, не имеющих дубликатов,
    и множество классов-дубликатов

    :param classes: Все классы, найденные в считывания АСТ.
    :return: кортеж из двух множеств: множества классов не-дубликатов и множество дубликатов
    """
    # Малоэффективная реализация со сложностью O(n^2)
    names = [decl.class_name for decl in classes]
    uniq = {decl for decl in classes if names.count(decl.class_name) == 1}
    dups = set(classes) - uniq
    return uniq, dups


def find_nonexistent_parents(classes: set[ClassDecl]) -> dict[ClassDecl, list[Parent]]:
    nonexistent: dict[ClassDecl, set[Parent]] = defaultdict(list)

    for decl in classes:
        for parent in decl.inherit:
            if not any(parent.class_name == c.class_name for c in classes):
                nonexistent[decl].append(parent)

    return nonexistent


def find_duplicated_parents(classes: set[ClassDecl]) -> dict[str, set[str]]:
    dups: dict[str, set[str]] = {}

    for decl in classes:
        pnames = [p.class_name for p in decl.inherit]
        same_parents = {pname for pname in pnames if pnames.count(pname) > 1}
        if same_parents:
            dups[decl.class_name] = same_parents

    return dups


def process_stage0(classes: list[ClassDecl]) -> set[ClassDecl]:
    uniq, dups = analyze_duplicates(classes)
    if dups:
        raise DuplicatesError(dups)

    nonexistent = find_nonexistent_parents(uniq)
    if nonexistent:
        raise ParentDoesNotExistError(nonexistent)

    return uniq