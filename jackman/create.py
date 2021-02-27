import os
import logging
from distutils.dir_util import copy_tree

from jackman.helpers import cd_is_project, get_cwd, Expects, get_jackman_dir


def main():
    """Creates a new project folder in the current directory
    """

    # TODO: Add more logging to this
    log = logging.getLogger(__name__)

    if cd_is_project():
        log.critical(f'Directory {get_cwd()} is already a project and Jackman projects should not be nested.')
    else:
        name = input('What is the name of your project? ')

        if os.path.exists(name) and os.path.isdir(name) and len(os.listdir(name)) != 0:
            log.critical(f'The specified directory already exists and contains files.')
            raise FileExistsError

        with Expects([FileExistsError]):
            os.mkdir(name)

        copy_tree(f'{get_jackman_dir()}/_templates/empty_project/', name)
