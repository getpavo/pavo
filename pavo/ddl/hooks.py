from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable


class HookTypes(Enum):
    BEFORE = auto()
    AFTER = auto()
    CUSTOM = auto()


@dataclass
class Invoker:
    module: str
    name: str


@dataclass
class Hook:
    func: Callable
    type_: HookTypes
    invoker: Invoker

    def __call__(self, *args, **kwargs):
        func(*args, **kwargs)
