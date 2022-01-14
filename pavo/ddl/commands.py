from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Command(ABC):
    name: str
    allow_outside_project: bool = False

    @abstractmethod
    def run(self, args: Optional[list] = None) -> None:
        ...
