from pavo.utils import context
import pytest


def test_expects() -> None:
    # Accepts a single error and handles it properly
    with context.Expects([ValueError]):
        raise ValueError()

    # Accepts multiple errors and handles one of these properly
    with context.Expects([ValueError, KeyError, AttributeError]):
        raise KeyError()

    # Accepts multiple errors, but throws when the error is not in the list
    with pytest.raises(NotImplementedError):
        with context.Expects([ValueError, KeyError]):
            raise NotImplementedError()

    # Accepts a single error, and returns when no error is thrown
    with context.Expects([ValueError]):
        x = 12
