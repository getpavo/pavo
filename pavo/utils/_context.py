from typing import Optional, Type
from types import TracebackType


class Expects:
    """Context manager when we are expecting that an error could occur, and we accept this.

    Args:
        expected_errors (list): A list of expected errors to skip.

    Raises:
        ValueError: The provided argument is not a list.

    Attributes:
        expected_errors (list): A list of expected errors to skip.
    """

    def __init__(self, expected_errors: list[Type[BaseException]]) -> None:
        if not isinstance(expected_errors, list):
            raise ValueError("Expected list as list of expected errors")
        self.expected_errors: list[Type[BaseException]] = expected_errors

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        err: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        if not err:
            return True
        if err in self.expected_errors:
            return True

        raise err
