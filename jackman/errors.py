class DeployError(Exception):
    pass


class DeployUnknownPipelineError(DeployError):
    pass


class CoreError(Exception):
    pass


class CoreUnspecifiedCommandError(CoreError):
    pass


class CoreUnknownCommandError(CoreError):
    pass


class CoreInvalidExecutionDirectory(CoreError):
    pass


class CoreHelpCommandTooLong(CoreError):
    pass


class CreateError(Exception):
    pass


class CreateMissingProjectNameError(CreateError):
    pass


class CreateNestedProjectError(CreateError):
    pass


class CreateDirectoryExistsNotEmptyError(CreateError):
    pass
