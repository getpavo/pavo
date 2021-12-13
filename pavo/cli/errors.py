from pavo.core.errors import PavoException


class CliError(PavoException):
    """Parent class of all errors that occur when using CLI."""


class UnspecifiedCommandError(CliError):
    """Please specify a command to run Pavo."""


class UnknownCommandError(CliError):
    """The specified command could not be found, are you sure it is imported?"""


class InvalidExecutionDirectoryError(CliError):
    """You are executing Pavo in an invalid Pavo project. Please create or navigate to a project."""
