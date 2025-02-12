from .tree.abstract_node import Location


class CompilerError(Exception):
    ERROR_COLOR = "\x1B[31m"
    BOLD_COLOR = "\033[1m"
    RESET_COLOR = "\x1B[0m"

    def __init__(self, desc: str, location: Location | None = None) -> None:
        self.desc = desc
        self.location = location

    def format_location(self) -> str:
        if self.location is None:
            return ""
        filename = self.location.filename or "<input>"
        return f"{filename}:{self.location.first_line}:{self.location.first_column}: "

    def __str__(self) -> str:
        return (f"{self.BOLD_COLOR}{self.format_location()}"
                f"{self.ERROR_COLOR}error: "
                f"{self.RESET_COLOR}{self.desc}")


class ErrorCollector:
    LINE_SEPARATOR = "\n\n"

    def __init__(self) -> None:
        self.errors = []

    def add_error(self, error: CompilerError) -> None:
        self.errors.append(error)

    def ok(self) -> bool:
        return len(self.errors) == 0

    def show(self) -> None:
        if self.ok(): return

        for error in self.errors:
            print(error, end=self.LINE_SEPARATOR)
            