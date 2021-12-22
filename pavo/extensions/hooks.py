from functools import wraps
from typing import Callable, Any

from pavo.cli import handle_message
from pavo.ddl.hooks import HookTypes, Hook, Invoker
from _errors import FunctionAlreadyRegisteredException


class HookManager:
    def __init__(self):
        self._hooks: dict[str, dict[str, list[Hook]]] = {}

    @property
    def hooks(self) -> dict[str, dict[str, list[Hook]]]:
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

    def execute(self, type_: HookTypes, name: str) -> None:
        for hook in self.hooks.get(name, {}).get(type_.name, []):
            hook()


global_hook_manager = HookManager()
