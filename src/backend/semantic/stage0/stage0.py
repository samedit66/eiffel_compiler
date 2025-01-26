from collections import defaultdict
from typing import Iterable

from ...tree.class_decl import ClassDecl, Parent

from ..base import SemanticError
from .errors import *


def find_duplicated_classes(classes: list[ClassDecl]) -> list[ClassDecl]:
    names = [decl.class_name for decl in classes]
    dups = [decl for decl in classes if names.count(decl.class_name) > 1]
    return dups


def find_nonexistent_parents(classes: Iterable[ClassDecl]) -> dict[ClassDecl, list[Parent]]:
    nonexistent: dict[ClassDecl, set[Parent]] = defaultdict(list)

    for decl in classes:
        for parent in decl.inherit:
            if not any(parent.class_name == c.class_name for c in classes):
                nonexistent[decl].append(parent)

    return nonexistent


def find_duplicated_parents(classes: list[ClassDecl]) -> dict[ClassDecl, list[Parent]]:
    dup_parents: dict[ClassDecl, list[Parent]] = {}

    for decl in classes:
        pnames = [p.class_name for p in decl.inherit]
        same_parents = [parent for parent in decl.inherit if pnames.count(parent.class_name) > 1]
        if same_parents:
            dup_parents[decl] = same_parents

    return dup_parents


def find_class_by_name(classes: list[ClassDecl], class_name: str) -> ClassDecl | None:
    try:
        return next(c for c in classes if c.class_name == class_name)
    except StopIteration:
        return None


def find_circular_inheritance_for(
        class_decl: ClassDecl | None,
        visited_parents: list[ClassDecl],
        ) -> list[ClassDecl]:
    """Ищет в иерархии заданного класса циклическое наследование.

    :param class_decl: Заданный класс.
    :param visited_parents: Последовательность посещенных родителей.
    :return: Пустой список, в случае если циклического наследования нет,
    иначе список классов, приводящих к изначальному class_decl.
    """
    if class_decl is None:
        return []

    for parent in class_decl.inherit:
        # Как только мы нашли родителя в уже посещенных классах,
        # значит циклическое наследование найдено
        if find_class_by_name(visited_parents, parent.class_name):
            return visited_parents + [parent.class_decl]
    
        # В ином случае пытаемся рекурсивно получить "цепь",
        # состоящую из родителей parent класса
        if chain := find_circular_inheritance_for(
                        parent.class_decl,
                        visited_parents + [parent.class_decl],
                        ):
            return chain
    
    return []


def find_circular_inheritance(classes: list[ClassDecl]) -> dict[ClassDecl, list[ClassDecl]]:
    chains: dict[ClassDecl, list[ClassDecl]] = {}

    for decl in classes:
        chain = find_circular_inheritance_for(decl, [decl])

        names = [c.class_name for c in chain]
        if names.count(decl.class_name) > 1:
            chains[decl] = chain

    return chains


def add_implicit_root_class(classes: list[ClassDecl], root_class: str = "ANY") -> None:
    root_parent = Parent(location=None, class_name=root_class)

    for decl in classes:
        if not decl.inherit and decl.class_name != root_class:
            decl.inherit.append(root_parent)


def set_class_decls(classes: list[ClassDecl]) -> None:
    for decl in classes:
        for parent in decl.inherit:
            try:
                parent.class_decl = next(
                    decl for decl in classes if decl.class_name == parent.class_name
                    )
            except StopIteration:
                pass


def process_stage0(ast: list[ClassDecl], root_class: str = "ANY") -> list[ClassDecl]:
    """Первая стадия семантического анализа состоит в следующем:
        1) Проверка, что отсутствуют дублированные декларации классов;
        2) Проверка, что все указанные родители существуют;
        3) Проверка, что корневой класс существует (с пунктом (2)
            объединять нельзя, т.к. все родители могут существовать, но среди
            переданных классов отсутствует тот, который является корневым);
        4) Проверка, что циклического наследования нет.

    Процедура мутирует переданный список классов: каждому классу, у которого нет
    явного родителя устанавливается ссылка на root_class, а каждому объекту Parent
    устанавливается ссылка class_decl.

    В случае выявление семантических ошибок процедура выбрасывает
    соответствующие исключения.

    Parameters
    ----------
    ast : list[ClassDecl]
        Абстрактное синтаксическое дерево - список классов программы
    root_class : str
        Название корневого класса
    """
    exps: list[SemanticError] = []

    dups = find_duplicated_classes(ast)
    if dups:
        exps.append(DuplicatesError(dups))

    nonexistent = find_nonexistent_parents(ast)
    if nonexistent:
        exps.append(NonexistentParentsError(nonexistent))

    dup_parents = find_duplicated_parents(ast)
    if dup_parents:
        exps.append(DuplicatedParentsError(dup_parents))

    if not find_class_by_name(ast, root_class):
        exps.append(MissingRootClassError(root_class))

    add_implicit_root_class(ast, root_class)

    set_class_decls(ast)

    self_inherited = find_circular_inheritance(ast)
    if self_inherited:
        exps.append(SelfInheritedError(self_inherited))
        
    if exps:
        raise ExceptionGroup("Semantic problems at stage 0", exps)
    
    return ast
    