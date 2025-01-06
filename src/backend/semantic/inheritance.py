from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque

from backend.tree.class_decl import ClassDecl, FeatureSection
from backend.tree.features import Feature


@dataclass
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


def hierarchy_for(
          needed_class: ClassDecl,
          all_classes: list[ClassDecl]
          ) -> list[ClassDecl]:
    hierarchy = []
    ancestors_to_visit = needed_class.inherit_section.ancestors

    while ancestors_to_visit:
        ancestor = ancestors_to_visit.pop(0)
        

    return hierarchy
