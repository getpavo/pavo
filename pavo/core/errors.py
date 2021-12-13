from typing import Optional


# Base Pavo Exception
class PavoException(Exception):
    """Pavo's BaseException-like Exception class, uses docstrings to set default error messages."""
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or self.__doc__)


# Parent errors
class CreateError(PavoException):
    """An error occurred running pavo:create."""


class DeployError(PavoException):
    """An error occurred running pavo:deploy."""


# Children errors
class MissingProjectNameError(CreateError):
    """Missing a project name. Command usage: "pavo create <name>"."""


class NestedProjectError(CreateError):
    """Unable to create a Pavo project inside another Pavo project."""


class DirectoryExistsNotEmptyError(CreateError):
    """The specified directory already exists and is currently not empty."""


class DeployUnknownPipelineError(DeployError):
    """The requested pipeline does not exist when deploying."""
