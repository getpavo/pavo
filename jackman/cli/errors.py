class CliError(Exception):
    """Parent class of all errors that occur when using CLI."""
    pass

class UnspecifiedCommandError(CliError):
    """Raised when no command is specified when executing jackman:core."""
    pass


class UnknownCommandError(CliError):
    """Raised when an unknown command is specified when executing jackman:core."""
    pass


class InvalidExecutionDirectoryError(CliError):
    """Raised when calling any other function than help or create from outside a Jackman project directory."""
    pass
