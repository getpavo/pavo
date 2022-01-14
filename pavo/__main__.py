from sys import argv
from pavo.app import _cli

if __name__ == '__main__':
    _cli._main(argv[1:])  # pylint: disable=protected-access
