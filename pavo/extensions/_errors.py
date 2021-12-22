from pavo.core import PavoException


class ExtensionError(PavoException):
    """Base exception for errors with Extensions and Plugins. Should not be raised directly."""


class FunctionAlreadyRegisteredException(ExtensionError):
    """The supplied function was already added as a hook to the HookManager."""
