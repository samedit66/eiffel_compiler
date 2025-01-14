from typing import Iterable, Callable


class SemanticError(Exception):
    """Корневой класс для всех ошибок,
    случившихся во время семантического анализа
    """


def duplicates[A, B](s: Iterable[A], f: Callable[[A], B] | None = None) -> set[A]:
    ...
