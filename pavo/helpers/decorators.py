from functools import wraps
from typing import Callable, Any


def allow_outside_project(func: Callable) -> Callable:
    """Marks a Pavo entry point as allowed to run outside a Pavo project."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    # Ignore type checking, custom attributes on callables are currently not supported.
    # See: https://github.com/python/mypy/issues/2087
    wrapper.allowed_outside_project = True  # type: ignore
    return wrapper
