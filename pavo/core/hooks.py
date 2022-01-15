from pavo.ddl.hooks import HookManagerInterface, HookTypes, Hook, Invoker
from pavo.core.exceptions import FunctionAlreadyRegisteredException


class HookManager(HookManagerInterface):
    """Manages the registration, execution and removal of method hooks."""

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
