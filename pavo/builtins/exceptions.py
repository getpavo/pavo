from pavo.core import PavoException


class MissingProjectNameError(PavoException):
    """Missing a project name. Command usage: "pavo create <name>"."""
    pass


class NestedProjectError(PavoException):
    """Unable to create a Pavo project inside another Pavo project."""
    pass


class DirectoryExistsNotEmptyError(PavoException):
    """The specified directory already exists and is currently not empty."""
    pass
