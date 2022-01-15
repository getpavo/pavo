from pavo.core import PavoException


class CliError(PavoException):
    """Parent class of all errors that occur when using CLI."""


class UnspecifiedCommandError(CliError):
    """Please specify a command to run Pavo."""



