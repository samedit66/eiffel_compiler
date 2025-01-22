from ...tree.class_decl import ClassDecl, Parent, Alias
from ...tree.features import Feature

from ..base import SemanticError


class InheritanceErrorGroup(SemanticError):

    def __init__(self, class_decl: ClassDecl, errors: dict[Parent, list[SemanticError]]) -> None:
        self.class_decl = class_decl
        self.errors_by_parent = errors
        super().__init__(self.message(class_decl, errors))

    @staticmethod
    def message(class_decl: ClassDecl, errors_by_parent: dict[Parent, list[SemanticError]]) -> str:
        if not errors_by_parent:
            return f"No inheritance errors detected for class '{class_decl.class_name}'."

        location_info = (
            f"on line {class_decl.location.first_line}" if class_decl.location.first_line == class_decl.location.last_line
            else f"between lines {class_decl.location.first_line} and {class_decl.location.last_line}"
        )

        msg_parts = [
            f"Inheritance errors detected in class '{class_decl.class_name}' defined in file '{class_decl.defined_in_file}' {location_info}:"
        ]

        for parent, errors in sorted(errors_by_parent.items(), key=lambda item: item[0].class_name):
            # Handle parent location details
            if parent.location is not None:
                parent_location_info = (
                    f"on line {parent.location.first_line}" if parent.location.first_line == parent.location.last_line
                    else f"between lines {parent.location.first_line} and {parent.location.last_line}"
                )
            else:
                parent_location_info = f"in file '{parent.class_decl.defined_in_file}' starting at line {parent.class_decl.location.first_line}"

            # Add parent class info
            msg_parts.append(
                f"  Parent class '{parent.class_name}' {parent_location_info} has the following issues:"
            )

            # Format errors with additional indentation
            for error in errors:
                error_message = str(error).replace("\n", "\n      ")
                msg_parts.append(f"    - {error_message}")

        return "\n".join(msg_parts)

    def __str__(self) -> str:
        return self.message(self.class_decl, self.errors_by_parent)


class DuplicateOriginalNameError(SemanticError):
    
    def __init__(self, aliases: list[Alias]) -> None:
        self.aliases = aliases
        super().__init__(str(self))

    @staticmethod
    def message_lines(aliases: list[Alias]) -> list[str]:
        msg_parts = ["Duplicate original names detected in renaming:"]
        grouped = {}

        # Группируем по original_name
        for alias in aliases:
            location_info = (
                f"on line {alias.location.first_line}"
                if alias.location.first_line == alias.location.last_line
                else f"between lines {alias.location.first_line} and {alias.location.last_line}"
            )
            grouped.setdefault(alias.original_name, []).append(location_info)

        # Формируем сообщение
        for original_name, locations in grouped.items():
            msg_parts.append(f"Original name '{original_name}' appears in:")
            for location in locations:
                msg_parts.append(f"  - {location}")
        
        return msg_parts
    
    def __str__(self) -> str:
        return "\n".join(self.message_lines(self.aliases))


class DuplicateAliasNameError(SemanticError):
    
    def __init__(self, aliases: list[Alias]) -> None:
        self.aliases = aliases
        super().__init__(str(self))
        
    @staticmethod
    def message_lines(aliases: list[Alias]) -> list[str]:
        msg_parts = ["Duplicate alias names detected in renaming:"]
        grouped = {}

        # Группируем по alias_name
        for alias in aliases:
            location_info = (
                f"on line {alias.location.first_line}"
                if alias.location.first_line == alias.location.last_line
                else f"between lines {alias.location.first_line} and {alias.location.last_line}"
            )
            grouped.setdefault(alias.alias_name, []).append(location_info)

        for alias_name, locations in grouped.items():
            msg_parts.append(f"Alias name '{alias_name}' conflicts in:")
            for location in locations:
                msg_parts.append(f"  - {location}")
        
        return msg_parts
    
    def __str__(self) -> str:
        return "\n".join(self.message_lines(self.aliases))


class RenameNonexistentFeatureError(SemanticError):
    
    def __init__(self, aliases: list[Alias]) -> None:
        self.aliases = aliases
        super().__init__(str(self))

    @staticmethod
    def message_lines(aliases: list[Alias]) -> list[str]:
        msg_parts = ["Attempted to rename one or more nonexistent features:"]
        grouped = {}

        # Группируем по original_name
        for alias in aliases:
            location_info = (
                f"on line {alias.location.first_line}"
                if alias.location.first_line == alias.location.last_line
                else f"between lines {alias.location.first_line} and {alias.location.last_line}"
            )
            grouped.setdefault(alias.original_name, []).append(location_info)

        for original_name, locations in grouped.items():
            msg_parts.append(f"Feature '{original_name}' was attempted to be renamed in:")
            for location in locations:
                msg_parts.append(f"  - {location}")
        
        return msg_parts

    def __str__(self) -> str:
        return "\n".join(self.message_lines(self.aliases))


class UndefineNonexistentFeatureError(SemanticError):

    def __init__(self, features: list[str]) -> None:
        self.features = features
        super().__init__(str(self))

    @staticmethod
    def message_lines(features: list[str]) -> list[str]:
        msg_parts = ["Attempted to undefine nonexistent features:"]
        for feature in features:
            msg_parts.append(f"  - {feature}")
        return msg_parts

    def __str__(self) -> str:
        return "\n".join(self.message_lines(self.features))


class TwiceDeferredFeatureError(SemanticError):
    
    def __init__(self, features: list[Feature]) -> None:
        self.features = features
        super().__init__(str(self))
        
    @staticmethod
    def message_lines(features: list[Feature]) -> list[str]:
        msg_parts = ["Features cannot be both undefined and declared as deferred:"]
        
        for feature in features:
            location_info = (
                f"on line {feature.location.first_line}"
                if feature.location.first_line == feature.location.last_line
                else f"between lines {feature.location.first_line} and {feature.location.last_line}"
            )
            msg_parts.append(
                f"  - Feature '{feature.name}' is listed in the 'undefine' section and "
                f"is also declared as deferred {location_info}"
            )
        
        return msg_parts

    def __str__(self) -> str:
        return "\n".join(self.message_lines(self.features))
    

class RedefineNonexistentFeatureError(SemanticError):
    """Ошибка: попытка переопределить функции, отсутствующие в родителе."""

    def __init__(self, nonexistent: list[str]) -> None:
        super().__init__(RedefineNonexistentFeatureError.message(nonexistent))
        self.nonexistent = nonexistent

    @staticmethod
    def message(nonexistent: list[str]) -> str:
        return (
            "Attempted to redefine features that do not exist in the parent class:\n"
            + "\n".join(f"  - {name}" for name in nonexistent)
        )
    
class FeatureNotDefinedError(SemanticError):
    """Ошибка: попытка переопределить функции, которые не определены или отложены."""

    def __init__(self, not_defined: list[Feature]) -> None:
        super().__init__(FeatureNotDefinedError.message(not_defined))
        self.not_defined = not_defined

    @staticmethod
    def message(not_defined: list[Feature]) -> str:
        msg_parts = ["Attempted to redefine features that are not properly defined:"]
        for feature in not_defined:
            location_info = (
                f"on line {feature.location.first_line}" if feature.location.first_line == feature.location.last_line
                else f"between lines {feature.location.first_line} and {feature.location.last_line}"
            )
            msg_parts.append(f"  - {feature.name} {location_info}")
        return "\n".join(msg_parts)


class TwiceListedFeatureError(SemanticError):
    """Ошибка: одна или несколько фич указаны несколько раз в секции (например, 'undefine')."""

    def __init__(self, twice_appeared: list[str], section_name: str) -> None:
        super().__init__(TwiceListedFeatureError.message(twice_appeared, section_name))
        self.twice_appeared = twice_appeared
        self.section_name = section_name

    @staticmethod
    def message(twice_appeared: list[str], section_name: str) -> str:
        """Формирует сообщение об ошибке для повторно указанных фич с секцией."""
        unique_features = sorted(set(twice_appeared))
        return (
            f"The following features were listed multiple times in the '{section_name}' section:\n"
            + "\n".join(f"  - {feature}" for feature in unique_features)
        )


class UnknownFeatureError(SemanticError):
    """Ошибка: фича, указанная в секции, не найдена в родителе."""

    def __init__(self, unknown_features: list[str], section_name: str) -> None:
        super().__init__(UnknownFeatureError.message(unknown_features, section_name))
        self.unknown_features = unknown_features
        self.section_name = section_name

    @staticmethod
    def message(unknown_features: list[str], section_name: str) -> str:
        """Формирует сообщение об ошибке для несуществующих фич в указанной секции."""
        unique_features = sorted(set(unknown_features))
        return (
            f"The following features were specified in the '{section_name}' section, but are not found in parent features:\n"
            + "\n".join(f"  - {feature}" for feature in unique_features)
        )
