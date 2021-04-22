import os
import requests
from yaml import dump as create_yaml
from pathlib import Path

from jackman.core.errors import MissingProjectNameError, NestedProjectError, DirectoryExistsNotEmptyError
from jackman.core.helpers import cd_is_project, Expects


def main(name=None, boilerplate=True):
    """Creates a new project folder in the current directory.

    This is one of the Jackman core functionalities, which lets a user create a new project.
    It currently does so by copying a template folder into the users file system, but it should
    be updated according to generate using a configuration file.

    Args:
        name (str): The name of the project that should be created.
        boilerplate (bool): Whether or not the boilerplate Jackman template should be installed.

    Raises:
        MissingProjectNameError: The project name was not specified.
        NestedProjectError: You are executing create in a Jackman project folder, leading to a nested project.
        DirectoryExistsNotEmptyError: The name of the project is an existing, non-empty directory.
    """
    if name is None:
        raise MissingProjectNameError

    if cd_is_project():
        raise NestedProjectError

    if os.path.exists(name) and os.path.isdir(name) and len(os.listdir(name)) != 0:
        raise DirectoryExistsNotEmptyError

    with Expects([FileExistsError]):
        os.mkdir(name)

    _create_new_project_structure(name)

    # copy_tree(f'{get_jackman_dir()}/_templates/empty_project/', name)

    if boilerplate:
        # TODO: Finish this so the Hyde theme is actually pulled
        request = requests.get('https://api.github.com/repos/jackmanapp/hyde/releases/latest')
        pass


def _create_new_project_structure(project_name):
    """Creates a project from the specified structure.

    The structure should be specified as an array of paths that start with a slash.
    It is allowed to nest paths in the structure, as they will be made recursively.
    It is also recommended to add a comment after the path, to show the intention for the path.

    Args:
        project_name (str): The name of the project that these files should be built for.

    Raises:
        DirectoryExistsNotEmptyError: The specified project directory is not empty.
    """
    if os.path.exists(project_name) and os.path.isdir(project_name) and len(os.listdir(project_name)) != 0:
        raise DirectoryExistsNotEmptyError

    structure = [
        '/_drafts/',        # Drafts of posts that should not be published yet
        '/_posts/',         # Blog-like posts
        '/_pages/',         # Pages of the website
        '/_public/',        # Files that should be untouched copied to the final build
        '/_templates/',     # For templates that should be used in the build
        '/_static/styles/', # For stylesheets in sass or css
        '/_static/images/'  # For images that should be optimized by the build process
    ]

    for directory in structure:
        Path(f'./{project_name}/{directory}').mkdir(parents=True, exist_ok=True)

    # Jackman configuration file
    default_config = {
        'meta': {
            'title': 'My Jackman Project',
            'suffix': 'MJP',
            'description': 'This is my new, amazing Jackman Project',
        },
        'build': {
            'optimize': {
                'minify_html': {
                    'remove_comments': True,
                    'remove_empty_space': True,
                    'remove_all_empty_space': False,
                    'reduce_empty_attributes': True,
                    'reduce_boolean_attributes': False,
                    'remove_optional_attribute_quotes': True,
                    'convert_charrefs': True,
                    'keep_pre': False,
                }
            }
        }
    }

    with open(f'./{project_name}/.jackman', 'x') as f:
        f.write(create_yaml(default_config))
