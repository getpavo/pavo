from sys import argv
from pavo.cli import _cli

if __name__ == '__main__':
    _cli._main(argv[1:])  # pylint: disable=protected-access
