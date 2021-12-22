from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Type, TypeVar

# TypeVar for the generation methods in the Invoker class.
_T = TypeVar('_T', bound='Invoker')


class HookTypes(Enum):
    BEFORE = auto()
    AFTER = auto()
    CUSTOM = auto()


@dataclass
class Invoker:
    module: str
    name: str

    @classmethod
    def from_callable(cls: Type[_T], func: Callable) -> _T:
        return cls(
            module=func.__module__,
            name=func.__qualname__
        )

    @property
    def unique_name(self):
        return f'{self.module}.{self.name}'


@dataclass
class Hook:
    func: Callable
    type: HookTypes
    invoker: Invoker

    def __call__(self, *args, **kwargs):
        func(*args, **kwargs)
