from typing import Iterable, Callable


class SemanticError(Exception):
    """Корневой класс для всех ошибок,
    случившихся во время семантического анализа
    """


def count[A, B](it: Iterable[A], value: B, key: Callable[[A], B] | None = None):
    mapped = it if key is None else [key(e) for e in it]
    return mapped.count(value)
