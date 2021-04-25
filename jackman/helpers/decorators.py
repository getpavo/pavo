from functools import wraps


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


def allow_outside_project(func):
    @wraps(func)
    def wrapper():
        func()

    wrapper.allowed_outside_project = True
    return wrapper
