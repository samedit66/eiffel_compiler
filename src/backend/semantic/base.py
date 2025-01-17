from typing import Iterable, Callable


class SemanticError(Exception):
    """Корневой класс для всех ошибок,
    случившихся во время семантического анализа
    """
