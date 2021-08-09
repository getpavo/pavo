from functools import wraps
from typing import Callable, Any

from pavo.cli import broadcast_message


_HOOKS: dict[Any, dict[Any, list]] = {}


def use_before(name: str) -> Callable:
    """Hooks into the "before execution" hook of specified function.

    Note:
        Hooks are not called in a specific order, but rather in the order they are discovered.
        This means you should not depend a hook to another hook, but only on the functionality.
        If you want to depend a hook on another hook, decorate the hook to depend on with @extensible.

    Args:
        name (str): The name of the function to hook into.

    Returns:
        Callable: the decorated function.
    """
    def decorator(func: Callable) -> Callable:
        _register_hook(func, 'before', name)
        return func
    return decorator


def use_after(name: str):
    """Hooks into the "after execution" hook of specified function.

    Note:
        Hooks are not called in a specific order, but rather in the order they are discovered.
        This means you should not depend a hook to another hook, but only on the functionality.
        If you want to depend a hook on another hook, decorate the hook to depend on with @extensible.

    Args:
        name (str): The name of the function to hook into.

    Returns:
        Callable: the decorated function.
    """
    def decorator(func: Callable) -> Callable:
        _register_hook(func, 'after', name)
        return func
    return decorator


def extensible(types_: list[str]) -> Callable:
    """Define a function to be extensible with hooks.

    All discovered hooks are called on execution of the function, if the function allows a hook of such type.

    TODO: Add 'runtime' hooks that functions can explicitly call.

    Args:
        types_ (list): List of types you allow the hooks to call.

    Returns:
        Callable: the decorated function.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            name = '.'.join([func.__module__, func.__qualname__])

            # Run the before hooks
            if 'before' in types_:
                _call_hooks('before', name)

            # Run the function
            output = func(*args, **kwargs)

            # Run the after hooks
            if 'after' in types_:
                _call_hooks('after', name)

            return output
        return wrapper
    return decorator


def _register_hook(func: Callable, type_: str, name: str) -> None:
    """Register a hook to the _HOOKS global dict.

    Args:
        func (Callable): The function that is called in the hook.
        type_ (str): The type of hook you want to register.
        name (str): The name of the function to hook into.

    Returns:
        None
    """
    if _HOOKS.get(name) is None:
        _HOOKS[name] = {}

    if _HOOKS[name].get(type_) is not None:
        _HOOKS[name][type_].append(func)
    else:
        _HOOKS[name][type_] = [func]


def _call_hooks(type_: str, name: str) -> None:
    """Call a type of hook for a named function.

    Args:
        type_ (str): The type of hook you want to call.
        name (str): The name of the function that is hooked into.

    Returns:
        None
    """
    for hook in _HOOKS.get(name, {}).get(type_, []):
        hook() if callable(hook) else broadcast_message('warn',
                                                        f'Could not call hook. "{hook.__name__}" is not callable.')
