from sys import argv
from pavo.app import PavoApp

if __name__ == '__main__':
    app = PavoApp()
    app.run(argv[1:])  # pylint: disable=protected-access
