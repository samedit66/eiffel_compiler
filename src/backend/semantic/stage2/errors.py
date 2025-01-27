class TypeMismatchError(Exception):
    """Исключение, возникающее при несоответствии типов."""
    def __init__(self, message: str):
        super().__init__(message)
