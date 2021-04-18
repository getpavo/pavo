# Parent errors
class CoreError(Exception):
    """Parent class of all errors that occur when calling on jackman:core."""
    # TODO: These errors will probably only be raised by CLI and might be moved later
    pass


class CreateError(Exception):
    """Parent class of all errors that occur when calling on jackman:create."""
    pass


class DeployError(Exception):
    """Parent class of all errors that occur when calling on jackman:deploy."""
    pass


# Children errors
class CoreUnspecifiedCommandError(CoreError):
    """Raised when no command is specified when executing jackman:core."""
    pass


class CoreUnknownCommandError(CoreError):
    """Raised when an unknown command is specified when executing jackman:core."""
    pass


class CoreInvalidExecutionDirectoryError(CoreError):
    """Raised when calling any other function than help or create from outside a Jackman project directory."""
    pass


class CreateMissingProjectNameError(CreateError):
    """Raised when trying to create a project without specifying a name."""
    pass


class CreateNestedProjectError(CreateError):
    """Raised when trying to create a project inside a current Jackman project directory."""
    pass


class CreateDirectoryExistsNotEmptyError(CreateError):
    """Raised when trying to create a project inside a directory that already exists and is not empty."""
    pass


class DeployUnknownPipelineError(DeployError):
    """Raised when an unknown, unspecified pipeline was requested."""
    pass
