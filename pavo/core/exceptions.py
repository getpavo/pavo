from typing import Optional


# Base Pavo Exception
class PavoException(Exception):
    """Pavo's BaseException-like Exception class, uses docstrings to set default error messages."""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or self.__doc__)


class FunctionAlreadyRegisteredException(PavoException):
    """The supplied function was already added as a hook to the HookManager."""


class UnknownCommandError(PavoException):
    """The specified command could not be found, are you sure it is imported?"""


class InvalidExecutionDirectoryError(PavoException):
    """You are executing Pavo in an invalid Pavo project. Please create or navigate to a project."""


class MessageTypeAlreadyExists(PavoException):
    """The message type you are trying to register, already exists."""
