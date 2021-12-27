from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Type, TypeVar, Any

# TypeVar for the generation methods in the Invoker class.
_T = TypeVar('_T', bound='Invoker')


class HookTypes(Enum):
    """Enum that contains the different types of Pavo hooks."""
    BEFORE = auto()
    AFTER = auto()
    CUSTOM = auto()


@dataclass
class Invoker:
    """Dataclass that describes the function or method that invokes the hook."""
    module: str
    name: str

    @classmethod
    def from_callable(cls: Type[_T], func: Callable) -> _T:
        """Creates an Invoker instance from a Callable method.

        Args:
            func (Callable): The function that should be used as Invoker.

        Returns:
            Invoker: the Invoker with the data belonging to the input Callable.
        """
        return cls(
            module=func.__module__,
            name=func.__qualname__
        )

    @property
    def unique_name(self) -> str:
        """Returns the unique name that is given to the Invoker."""
        return f'{self.module}.{self.name}'


@dataclass
class Hook:
    """Dataclass that describes the structure of a Pavo plugin hook."""
    func: Callable
    type: HookTypes
    invoker: Invoker

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.func(*args, **kwargs)
