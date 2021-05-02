from functools import wraps


def singleton(class_):
    """Singleton decorator for classes.

    This decorator ensures there exists only one single entity of a class, which allows sharing of data by
    accessing the class as a sort of global variable.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


def allow_outside_project(func):
    """Marks a Jackman entry point as allowed outside of Jackman"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

    wrapper.allowed_outside_project = True
    return wrapper
