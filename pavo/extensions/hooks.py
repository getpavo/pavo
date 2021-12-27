from pavo.ddl.hooks import HookTypes, Hook, Invoker
from pavo.extensions._errors import FunctionAlreadyRegisteredException


class HookManager:
    """Manages the registration, execution and removal of method hooks."""
    def __init__(self) -> None:
        self._hooks: dict[str, dict[str, list[Hook]]] = {}

    @property
    def hooks(self) -> dict[str, dict[str, list[Hook]]]:
        """Getter for the _hooks class variable."""
        return self._hooks

    def register(self, hook: Hook) -> bool:
        """Register a hook to the hook manager.

        Args:
            hook (Hook): The hook to register to the manager.

        Raises:
            FunctionAlreadyRegisteredException: the hook was already registered to the function in the manager.

        Returns:
            bool: If registration has succeeded.
        """
        registered_hooks = self.hooks.get(hook.invoker.unique_name)

        # If there is no hook for a function, we should create the dict with possible types.
        if registered_hooks is None:
            registered_hooks = {x.name: [] for x in HookTypes}

        if hook in registered_hooks[hook.type.name]:
            raise FunctionAlreadyRegisteredException

        # Finally, update the hook mapping with the newly registered hooks
        registered_hooks[hook.type.name].append(hook)
        self.hooks[hook.invoker.unique_name] = registered_hooks

        return True

    def execute(self, type_: HookTypes, invoker: Invoker) -> None:
        """Executes the hooks that belong to a certain Invoker.

        Args:
            type_ (HookTypes): The type of hooks that should be executed.
            invoker (Invoker): The method that invoked the hooks.
        """
        for hook in self.hooks.get(invoker.unique_name, {}).get(type_.name, []):
            hook()


global_hook_manager = HookManager()


def register_hook(hook: Hook) -> bool:
    """Shortcut method for global_hook_manager.register()

    Args:
        hook (Hook): The hook to register to the global hook manager.

    Returns:
        bool: Whether registration was successful.
    """
    return global_hook_manager.register(hook)
