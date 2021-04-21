# Parent errors
class CreateError(Exception):
    """Parent class of all errors that occur when calling on jackman:create."""
    pass


class DeployError(Exception):
    """Parent class of all errors that occur when calling on jackman:deploy."""
    pass


# Children errors
class MissingProjectNameError(CreateError):
    """Raised when trying to create a project without specifying a name."""
    pass


class NestedProjectError(CreateError):
    """Raised when trying to create a project inside a current Jackman project directory."""
    pass


class DirectoryExistsNotEmptyError(CreateError):
    """Raised when trying to create a project inside a directory that already exists and is not empty."""
    pass


class DeployUnknownPipelineError(DeployError):
    """Raised when an unknown, unspecified pipeline was requested."""
    pass
