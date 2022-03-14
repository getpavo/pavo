import os
from typing import Optional
from pathlib import Path
from dataclasses import dataclass

from yaml import dump as create_yaml

from pavo.ddl.commands import CommandInterface
from pavo.utils import files, context
from .exceptions import MissingProjectNameError, NestedProjectError, DirectoryExistsNotEmptyError


@dataclass
class Create(CommandInterface):
    """Built-in 'create' command."""
    name: str = 'create'
    help: str = 'Creates a new project folder in the current directory.'
    allow_outside_project: bool = True

    def run(self, args: Optional[list] = None) -> None:
        """Creates a new Pavo project directory, with a default configuration.

        Args:
            args: The arguments provided by the caller.
        """
        if args is None:
            _create()
        else:
            _create(*args)


def _create(name: Optional[str] = None) -> None:
    """Creates a new project folder in the current directory.

    This is one of the Pavo core functionalities, which lets a user create a new project.

    Note:
        To change the behaviour of creating a project, hook into the 'pavo.core.create.main' function.

    Args:
        name (str): The name of the project that should be created.

    Raises:
        MissingProjectNameError: The project name was not specified.
        NestedProjectError: You are executing create in a Pavo project folder, leading to a nested project.
        DirectoryExistsNotEmptyError: The name of the project is an existing, non-empty directory.
    """
    if name is None:
        raise MissingProjectNameError

    if files.cd_is_project():
        raise NestedProjectError

    if os.path.exists(name) and os.path.isdir(name) and len(os.listdir(name)) != 0:
        raise DirectoryExistsNotEmptyError

    with context.Expects([FileExistsError]):
        os.mkdir(name)

    _create_new_project_structure(name)


def _create_new_project_structure(project_name: str) -> None:
    """Creates a project from the specified structure.

    The structure should be specified as an array of paths that start with a slash.
    It is allowed to nest paths in the structure, as they will be made recursively.

    Args:
        project_name (str): The name of the project that these files should be built for.

    Raises:
        DirectoryExistsNotEmptyError: The specified project directory is not empty.
    """
    if os.path.exists(project_name) and os.path.isdir(project_name) and len(os.listdir(project_name)) != 0:
        raise DirectoryExistsNotEmptyError

    structure = [
        '/_data/',               # Yaml-files with data that should be used on the site.
        '/_drafts/',             # Drafts of posts that should not be published yet.
        '/_posts/',              # Blog-like posts.
        '/_pages/',              # Pages of the website.
        '/_static/public/',      # Files that should be untouched and copied to the final build.
        '/_static/templates/',   # For templates that should be used in the build.
        '/_static/styles/',      # For stylesheets in sass or css.
        '/_static/images/',      # For images that should be optimized by the build process.
        '/_static/scripts/',     # For JavaScript that should be optimized by the build process.
        '/_plugins/'             # For Pavo plugin scripts that should be used.
    ]

    for directory in structure:
        Path(f'./{project_name}/{directory}').mkdir(parents=True, exist_ok=True)

    # Website meta file
    website_meta = {
        'title': project_name,
        'tagline': 'Built with Pavo',
        'description': 'This is my new, amazing Pavo Project'
    }

    with open(f'./{project_name}/_data/site.yaml', 'x', encoding='utf-8') as file:
        file.write(create_yaml(website_meta))

    # Advanced Pavo configuration file
    default_config = {
        'version': '0.1.0',
        'build': {
            'default_templates': {
                'page': 'page',
                'post': 'post',
                'draft': 'page'
            },
            'max_template_cache': 50,
            'markdown': {
                'extras': [
                    'cuddled-lists',
                    'fenced-code-blocks'
                ]
            },
            'paths': {
                'site_config': './_data/site.yaml'
            }
        },
        'logging': {
            'enabled': True,
            'level': 20
        },
        'plugins': None,
    }

    with open(f'./{project_name}/pavoconfig.yaml', 'x', encoding='utf-8') as file:
        file.write(create_yaml(default_config))
