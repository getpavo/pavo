import os
import requests
from distutils.dir_util import copy_tree

from jackman.core.errors import MissingProjectNameError, NestedProjectError, DirectoryExistsNotEmptyError
from jackman.core.helpers import cd_is_project, Expects, get_jackman_dir


def main(name=None, boilerplate=True):
    """Creates a new project folder in the current directory.
    """
    if name is None:
        raise MissingProjectNameError

    if cd_is_project():
        raise NestedProjectError

    if os.path.exists(name) and os.path.isdir(name) and len(os.listdir(name)) != 0:
        raise DirectoryExistsNotEmptyError

    with Expects([FileExistsError]):
        os.mkdir(name)

    copy_tree(f'{get_jackman_dir()}/_templates/empty_project/', name)

    if boilerplate:
        # TODO: Finish this so the Hyde theme is actually pulled
        request = requests.get('https://api.github.com/repos/jackmanapp/hyde/releases/latest')
        pass
