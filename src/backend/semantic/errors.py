from typing import Iterable
from itertools import groupby

from .base import SemanticError
from ..tree.class_decl import ClassDecl, Parent


class DuplicatesError(SemanticError):
    """Ошибка, возникающая в ходе обнаружения классов-дубликатов
    найденных в системе, либо в секции наследования
    """

    def __init__(self, dups: Iterable[ClassDecl]) -> None:
        super().__init__(DuplicatesError.message(dups))
        self.dups = dups

    @staticmethod
    def message(dups: Iterable[ClassDecl]) -> str:
        msg_parts = ["Found duplicated classes:"]

        for _, group in groupby(dups, key=lambda decl: decl.class_name):
            for dup in sorted(group, key=lambda decl: decl.location.first_line):
                msg_parts.append(
                    f"    {dup.class_name} in file {dup.defined_in_file}, line {dup.location.first_line}"
                    )

        return "\n".join(msg_parts)


class NonexistentParentsError(SemanticError):
    """Ошибка, возникающая, если класс наследуется от неизвестного родителя"""

    def __init__(self, nonexistent: dict[ClassDecl, list[Parent]]) -> None:
        super().__init__(NonexistentParentsError.message(nonexistent))
        self.nonexistent = nonexistent

    @staticmethod
    def message(nonexistent: dict[ClassDecl, list[Parent]]) -> str:
        msg_parts = ["Found nonexistent parents:"]

        for decl in sorted(nonexistent, key=lambda decl: decl.class_name):
            msg_parts.append(f"For class {decl.class_name} in file {decl.defined_in_file}:")

            for parent in nonexistent[decl]:
                msg_parts.append(f"    Parent {parent.class_name}, line {parent.location.first_line}")

        return "\n".join(msg_parts)


class DuplicatedParentsError(SemanticError):
    
    def __init__(self, dup_parents: dict[ClassDecl, list[Parent]]) -> None:
        super().__init__(DuplicatedParentsError.message(dup_parents))
        self.dup_parents = dup_parents

    @staticmethod
    def message(dup_parents: dict[ClassDecl, list[Parent]]) -> str:
        msg_parts = ["Found duplicated parents:"]

        for decl, parents in sorted(dup_parents.items(), key=lambda pair: pair[0].class_name):
            msg_parts.append(f"For class {decl.class_name} in file {decl.defined_in_file}:")

            for parent in parents:
                msg_parts.append(f"    Parent {parent.class_name}, line {parent.location.first_line}")

        return "\n".join(msg_parts)


class SelfInheritedError(SemanticError):
    
    def __init__(self, self_inherited: dict[ClassDecl, list[ClassDecl]]) -> None:
        super().__init__(SelfInheritedError.message(self_inherited))

    @staticmethod
    def message(self_inherited: dict[ClassDecl, list[ClassDecl]]) -> str:
        msg_parts = ["Found circular inheritance:"]

        for decl, chain in sorted(self_inherited.items(), key=lambda pair: pair[0].class_name):
            msg_parts.append(f"For class {decl.class_name} in file {decl.defined_in_file}, line {decl.location.first_line}:")
            
            msg_chain = " => ".join(decl.class_name for decl in chain)
            msg_parts.append(f"    Chain: {msg_chain}")

        return "\n".join(msg_parts)


class MissingRootClassError(SemanticError):

    def __init__(self, root_class: str) -> None:
        super().__init__(MissingRootClassError.message(root_class))

    @staticmethod
    def message(root_class: str) -> str:
        return f"Couldn't find root class {root_class}"
    