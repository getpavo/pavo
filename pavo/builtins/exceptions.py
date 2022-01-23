from pavo.core.exceptions import PavoException


class MissingProjectNameError(PavoException):
    """Missing a project name. Command usage: "pavo create <name>"."""


class NestedProjectError(PavoException):
    """Unable to create a Pavo project inside another Pavo project."""


class DirectoryExistsNotEmptyError(PavoException):
    """The specified directory already exists and is currently not empty."""
