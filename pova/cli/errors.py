class CliError(Exception):
    """Parent class of all errors that occur when using CLI."""
    pass


class UnspecifiedCommandError(CliError):
    """Raised when no command is specified when executing jackman:core."""
    pass


class UnknownCommandError(CliError):
    """Raised when an unknown command is specified when executing jackman:core."""
    def __init__(self, message='The specified command could not be found, are you sure it is imported?'):
        super().__init__(message)


class InvalidExecutionDirectoryError(CliError):
    """Raised when calling any other function than help or create from outside a Jackman project directory."""
    def __init__(self, message='You are executing Jackman in an invalid Jackman project. Please create a new project '
                               'or navigate to a valid project directory.'):
        super().__init__(message)
