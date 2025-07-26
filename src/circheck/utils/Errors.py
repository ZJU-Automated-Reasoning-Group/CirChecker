from dataclasses import dataclass
from antlr4.error.ErrorListener import ConsoleErrorListener, ErrorListener


class NewErrorListener(ConsoleErrorListener):
    INSTANCE = None

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxException("Error on line " + str(line) +
                              " col " + str(column) + ": " + offendingSymbol.text)


NewErrorListener.INSTANCE = NewErrorListener()


class SyntaxException(Exception):
    def __init__(self, msg):
        self.message = msg


class UnclosedComment(Exception):
    """Error raised when a comment is not closed."""

    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def __str__(self):
        return f"Unclosed comment at line {self.line}, column {self.column}."


class StaticError(Exception):
    """Base class for static errors."""
    pass


class NoMainFoundInProject(StaticError):
    """Error raised when no main function is found in the project."""

    def __str__(self):
        return "No main function found in the project."


@dataclass
class IncludeNotFound(StaticError):
    """Error raised when an include file is not found."""
    filename: str

    def __str__(self):
        return f"Include file '{self.filename}' not found."


class MultipleMainFound(StaticError):
    """Error raised when multiple main functions are found in the project."""

    def __str__(self):
        return "Multiple main functions found in the project."
