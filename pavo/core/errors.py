# Parent errors
class CreateError(Exception):
    """Parent class of all errors that occur when calling on pavo:create."""
    pass


class DeployError(Exception):
    """Parent class of all errors that occur when calling on pavo:deploy."""
    pass


# Children errors
class MissingProjectNameError(CreateError):
    """Raised when trying to create a project without specifying a name."""
    def __init__(self, message='Missing a project name. Command usage: "pavo create <name>".'):
        super().__init__(message)


class NestedProjectError(CreateError):
    """Raised when trying to create a project inside a current Pavo project directory."""
    def __init__(self, message='Unable to create a Pavo project inside another Pavo project.'):
        super().__init__(message)


class DirectoryExistsNotEmptyError(CreateError):
    """Raised when trying to create a project inside a directory that already exists and is not empty."""
    def __init__(self, message='The specified directory already exists and is currently not empty.'):
        super().__init__(message)


class DeployUnknownPipelineError(DeployError):
    """Raised when an unknown, unspecified pipeline was requested."""
