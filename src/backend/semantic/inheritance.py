from __future__ import annotations
from dataclasses import dataclass, field

from tree.class_decl import ClassDecl
from tree.features import Feature
from tree.class_decl.types import Parent


@dataclass(match_args=True, kw_only=True)
class FeatureRecord:
    """Описание фичи в таблице"""
    class_name: str
    """Имя класса, в котором фича была определена или объявлена"""
    feature_name: str
    """Имя фичи"""
    feature_node: Feature
    """Ссылка на узел абстрактного синтаксического дерева фичи"""


@dataclass
class FeatureFlatTable:
    """Таблица фич для класса"""
    table: list[FeatureRecord] = field(default_factory=list)

    def get_feature_node(
            self,
            feature_name: str,
            class_name: str | None = None,
            ) -> Feature | None:
        """Возвращает узел абстрактного синтаксического дерева фичи,
        либо None, если такой фичи не найдено. Поиск может производится
        с учетом класса-родителя, в котором эта фича должна быть определена.

        :param feature_name: Имя фичи
        :param class_name: Имя класса, в котором эта фича должна быть определена.
        Используется для реализации полиморфизма
        :return: Узел фичи или None, если такой фичи нет
        """
        # Поиск производится в порядке обратном порядку добавления в таблицу,
        # чтобы в случае отсутствия class_name, возвращался самый последний
        # определенный метод с таким именем
        for feature_record in reversed(self.table):
            if (feature_record.feature_name == feature_name and 
                (class_name is None or feature_record.class_name == class_name)):
                    return feature_name

        return None

    def add_feature_record(self, feature_record: FeatureRecord) -> None:
        self.table.append(feature_record)


class InheritanceError(Exception): pass


class DuplicatesError(Exception): pass


class UnknownParentError(InheritanceError): pass


def analyze_duplicates(
        classes: list[ClassDecl],
        ) -> tuple[set[ClassDecl], set[ClassDecl]]:
    dups = set()
    for c in classes:
        if c not in dups:
            dups.add(c)

    unique = set(classes) - dups
    return unique, dups


def hierarchy_for(
          needed_class: ClassDecl,
          all_classes: set[ClassDecl],
          root: str = "ANY",
          ) -> list[ClassDecl]:
    """Выполняет построение иерархии дерева наследования
    для заданного класса.
    
    :param needed_class: Заданный класс.
    :param all_classes: Множество всех классов в программе.
    :param root: Имя корневного класса. По умолчанию - `ANY`.
    :return: список классов, создающих иерархию, начиная 
    от прямых родителей и заканчивая корневым классом.
    """
    if not any(class_decl.class_name == root for class_decl in all_classes):
        raise UnknownParentError(f"Root class {root} wasn't found")
    
    parents = needed_class.inherit

    # Алгоритм построения иерархии наследования заключается в следующем:
    # 1) В качестве списка родителей принять прямых родителей класса.
    # 2) Добавить в иерархию первого родителя из списка, если его еще не было в иерархии.
    # 3) Пополнить список родителей всеми родителями родителя.
    # 4) Повторять пункт 2 до тех пор, пока список родителей не пустой.
    hierarchy = []
    while parents:
        parent = parents.pop(0)
        
        pname = parent.class_name
        try:
            pclass = next(class_decl for class_decl in all_classes if class_decl.class_name == pname)
        except StopIteration:
            raise UnknownParentError(f"Parent class {pname} wasn't found")
        
        if pclass not in hierarchy:
            hierarchy.append(pclass)

        parents.extend(pclass.inherit)

    return hierarchy


def flat(given_class: ClassDecl, all_classes: set[ClassDecl]) -> list[FeatureRecord]:
    if not given_class.inherit:
        return [
            FeatureRecord(
                class_name=given_class.class_name,
                feature_name=feature.name,
                feature_node=feature,
                )
            for feature in given_class.features
        ]
    
    flatten = []
    for parent in given_class.inherit:
        try:
            pclass = next(
                class_decl
                for class_decl in all_classes
                if class_decl.class_name == parent.class_name
                )
        except StopIteration:
            raise UnknownParentError(f"Parent class {parent.class_name} wasn't found") from None
        
        flatten.extend(flat(pclass, all_classes))
    
    flatten.extend(given_class.features)
    return flatten


def analyze_inheritance(classes: list[ClassDecl]):
    unique, dups = analyze_duplicates(classes)
    if dups:
        raise DuplicatesError()
