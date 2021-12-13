from functools import wraps
from typing import Callable, Any


def singleton(class_: Callable) -> Callable:
    """Singleton decorator for classes.

    This decorator ensures there exists only one single entity of a class, which allows sharing of data by
    accessing the class as a sort of global variable.
    """
    instances = {}

    def get_instance(*args: Any, **kwargs: Any) -> Callable:
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


def allow_outside_project(func: Callable) -> Callable:
    """Marks a Pavo entry point as allowed to run outside a Pavo project."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    wrapper.allowed_outside_project = True
    return wrapper
