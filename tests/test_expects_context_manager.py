import pytest
from jackman.helpers import *


def test_expects_input_not_list():
    with pytest.raises(ValueError):
        with Expects(KeyError):
            raise Exception


def test_expects_catch_error():
    with Expects([ZeroDivisionError]):
        print(10 / 0)


def test_expects_catch_error_multiple():
    with Expects([ZeroDivisionError, KeyError]):
        print(10 / 0)


def test_expects_no_error():
    with Expects([KeyError]):
        a = 2
        b = 4
        c = a * b + 10
        print(c)

    assert c == 18

def test_expects_different_error():
    test_dict = {
        'test': 'test_value',
        'second_key': 'second_value'
    }
    with pytest.raises(KeyError):
        with Expects([AttributeError]):
            print(test_dict['third'])
