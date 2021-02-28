import os
import logging
import requests
from distutils.dir_util import copy_tree

from jackman.errors import CreateMissingProjectNameError, CreateNestedProjectError, CreateDirectoryExistsNotEmptyError
from jackman.helpers import cd_is_project, Expects, get_jackman_dir

# TODO: Do something with this logging
log = logging.getLogger(__name__)


def main(name=None, get_hyde=True):
    """Creates a new project folder in the current directory.
    """
    if name is None:
        raise CreateMissingProjectNameError

    if cd_is_project():
        raise CreateNestedProjectError

    if os.path.exists(name) and os.path.isdir(name) and len(os.listdir(name)) != 0:
        raise CreateDirectoryExistsNotEmptyError

    with Expects([FileExistsError]):
        os.mkdir(name)

    copy_tree(f'{get_jackman_dir()}/_templates/empty_project/', name)

    if get_hyde:
        # TODO: Finish this so the Hyde theme is actually pulled
        request = requests.get('https://api.github.com/repos/jackmanapp/hyde/releases/latest')
        pass
