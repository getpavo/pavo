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
