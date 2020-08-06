import os


def get_cwd():
    return os.getcwd()


def get_sd():
    return os.path.dirname(os.path.abspath(__file__))


def set_dir(directory):
    try:
        os.chdir(str(directory))
        return True
    except OSError:
        return False
