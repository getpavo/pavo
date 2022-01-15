from functools import wraps
from typing import Callable, Any

from pavo.ddl.hooks import Hook, HookTypes, Invoker

# Temporary variable
# TODO: Remove this
global_hook_manager = object()


def use_before(module: str, name: str) -> Callable:
    """Hooks into the "before execution" hook of specified function.

    Note:
        Hooks are not called in a specific order, but rather in the order they are discovered.
        This means you should not depend on a hook to fire after another hook.
        If you want to depend a hook on another hook, decorate the hook to depend on with @extensible.

    Args:
        module (str): The module of the function to hook into.
        name (str): The qualname of the function to hook into.

    Returns:
        Callable: the decorated function.
    """
    def decorator(func: Callable) -> Callable:
        global_hook_manager.register(Hook(
            type=HookTypes.BEFORE,
            func=func,
            invoker=Invoker(
                module=module,
                name=name
            )
        ))
        return func
    return decorator


def use_after(module: str, name: str) -> Callable:
    """Hooks into the "after execution" hook of specified function.

    Note:
        Hooks are not called in a specific order, but rather in the order they are discovered.
        This means you should not depend on a hook to another hook, but only on the functionality.
        If you want to depend a hook on another hook, decorate the hook to depend on with @extensible.

    Args:
        module (str): The module of the function to hook into.
        name (str): The qualname of the function to hook into.

    Returns:
        Callable: the decorated function.
    """
    def decorator(func: Callable) -> Callable:
        global_hook_manager.register(Hook(
            type=HookTypes.AFTER,
            func=func,
            invoker=Invoker(
                module=module,
                name=name
            )
        ))
        return func
    return decorator


def extensible(types: list[HookTypes]) -> Callable:
    """Define a function to be extensible with hooks.

    All discovered hooks are called on execution of the function, if the function allows a hook of such type.

    Args:
        types (list): List of types you allow the hooks to call.

    Returns:
        Callable: the decorated function.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            invoker = Invoker.from_callable(func)

            # Run the before hooks
            if HookTypes.BEFORE in types:
                global_hook_manager.execute(HookTypes.BEFORE, invoker)

            # Run the function
            output = func(*args, **kwargs)

            # Run the after hooks
            if HookTypes.AFTER in types:
                global_hook_manager.execute(HookTypes.AFTER, invoker)

            return output
        return wrapper
    return decorator
