from collections import defaultdict
from typing import Iterable

from ..tree.class_decl import ClassDecl

from ..errors import ErrorCollector, CompilerError


def check_duplicated_classes(classes: list[ClassDecl]) -> None:
    """
    Проверяет, что не встречается более одного объявления класса с одинаковым именем.
    Если найден дубликат, бросается CompilerError с информацией об ошибке.
    """
    seen = {}
    for decl in classes:
        if decl.class_name in seen:
            # Используем location текущего объявления (можно и первое дублированное)
            raise CompilerError(
                f"Duplicate class declaration: '{decl.class_name}'", decl.location
            )
        seen[decl.class_name] = decl


def check_nonexistent_parents(classes: Iterable[ClassDecl]) -> None:
    """
    Проверяет, что для каждого родителя указанного в секции наследования существует объявление класса.
    Если находится ссылка на несуществующий класс, бросается CompilerError.
    """
    valid_names = {decl.class_name for decl in classes}
    for decl in classes:
        for parent in decl.inherit:
            if parent.class_name not in valid_names:
                raise CompilerError(
                    f"Class '{decl.class_name}' inherits from undefined class '{parent.class_name}'",
                    decl.location,
                )


def check_duplicated_parents(classes: list[ClassDecl]) -> None:
    """
    Проверяет, что в списке родителей одного класса нет повторяющихся записей.
    При обнаружении дублированного родителя бросается CompilerError.
    """
    for decl in classes:
        seen = set()
        for parent in decl.inherit:
            if parent.class_name in seen:
                raise CompilerError(
                    f"Class '{decl.class_name}' has duplicate parent declaration: '{parent.class_name}'",
                    decl.location,
                )
            seen.add(parent.class_name)


def _check_circular_inheritance_for(
    class_decl: ClassDecl,
    visited: list[ClassDecl],
    class_map: dict[str, ClassDecl]
) -> list[ClassDecl]:
    """
    Рекурсивная функция для поиска цикла в иерархии наследования.
    Если найден цикл, возвращается список классов (цепочка наследования),
    приводящая к циклическому подключению.
    Если цикл не обнаружен, возвращается пустой список.
    """
    for parent in class_decl.inherit:
        parent_decl = class_map.get(parent.class_name)
        if parent_decl is None:
            continue

        if any(v.class_name == parent_decl.class_name for v in visited):
            return visited + [parent_decl]

        cycle = _check_circular_inheritance_for(parent_decl, visited + [parent_decl], class_map)
        if cycle:
            return cycle

    return []


def check_circular_inheritance(classes: list[ClassDecl]) -> None:
    """
    Проверяет, что в системе классов отсутствует циклическое наследование.
    При обнаружении цикла бросается CompilerError с описанием цепочки.
    """
    class_map = {decl.class_name: decl for decl in classes}

    for decl in classes:
        cycle = _check_circular_inheritance_for(decl, [decl], class_map)
        if cycle:
            # Формируем читаемую цепочку, например: A -> B -> C -> A
            cycle_names = " -> ".join(c.class_name for c in cycle)
            raise CompilerError(
                f"Circular inheritance detected: {cycle_names}",
                decl.location,
            )


def examine_system(classes: list[ClassDecl], error_collector: ErrorCollector) -> None:
    """
    Первая стадия семантического анализа.
    Проверяет:
      1) Отсутствие дублированных деклараций классов;
      2) Существование всех указанных родителей;
      3) Отсутствие дублированных записей родителей;
      4) Отсутствие циклического наследования.
      
    При возникновении первой ошибки бросается CompilerError, который добавляется в ErrorCollector.
    """
    try:
        check_duplicated_classes(classes)
        check_nonexistent_parents(classes)
        check_duplicated_parents(classes)
        check_circular_inheritance(classes)
    except CompilerError as error:
        error_collector.add_error(error)
