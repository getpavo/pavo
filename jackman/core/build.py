import os
import shutil
import time
import glob
from datetime import datetime

import sass
import frontmatter
import markdown2

from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from distutils.dir_util import copy_tree
from treeshake import Shaker

from jackman.cli import broadcast_message
from jackman.helpers.context import Expects
from jackman.helpers.files import load_files, set_dir, get_cwd, cd_is_project, force_create_empty_directory
from jackman.helpers.config import get_config_value


class Builder:
    """Builder class for Jackman projects. Builds a website from project files.

    Args:
        mode (str): Type of build. Defaults to 'production' - which dispatches the build to _website directory.

    Attributes:
        mode (str): Type of build. Defaults to 'production' - which dispatches the build to _website directory.
        tmp_dir (str): Path to the temporary directory used for building before dispatching.
        jinja_environment (jinja2.environment): The Jinja environment to use when building.
    """

    def __init__(self, mode="production"):
        self.mode = mode
        self.directory = get_cwd() if cd_is_project() else None
        self.config = get_config_value('build')
        self.images = {}
        self.site = {
            'title': get_config_value('meta.title'),
            'tagline': get_config_value('meta.tagline'),
            'pages': {},
            'posts': {}
        }

        # Create a temporary folder to write the build to, so we can rollback at any time
        self.tmp_dir = f'_tmp_{int(time.time())}'
        os.mkdir(self.tmp_dir, 0o755)
        broadcast_message('echo', f'Created temporary directory with name {self.tmp_dir}')
        self.jinja_environment = None

    def build(self):
        """Public build function. Call to this function builds the project directory to _website.

        Returns:
            None
        """
        broadcast_message('info', 'Time to build a website!', header=True)
        if not cd_is_project():
            set_dir(self.directory)

        # Load all templates and set up a jinja environment
        self._load_templates()
        self.jinja_environment = self._create_jinja_env()

        # Copy all files from the public folder directly to the build directory
        for file in load_files('./_static/public/'):
            self._copy_to_tmp(f'./_static/public/{file}')

        # Build commands
        self._build_images()
        self._build_pages()
        self._build_posts()
        self._build_styles()
        self._optimize_styles()
        self._clean_tmp()

        if not self.mode == 'development' and not self.mode == 'dev':
            self._dispatch_build()

    def _copy_to_tmp(self, path, sub_folder=None):
        """Copies a file to the temporary working directory.

        Args:
            path (str): The relative path to the file to copy.
            sub_folder (str): The directory in the temporary directory to copy the file to. Defaults to ''.

        Returns:
            None
        """
        if sub_folder is not None:
            if not os.path.exists(f'{self.tmp_dir}/{sub_folder}'):
                os.mkdir(f'{self.tmp_dir}/{sub_folder}/')
            shutil.copy(path, f'{self.tmp_dir}/{sub_folder}')
        else:
            shutil.copy(path, f'{self.tmp_dir}/')

    def _build_images(self):
        """Copies images to the temporary folder.

        TODO: We should add some image optimization in here, because this can be improved by a lot.
        """
        force_create_empty_directory(f'{self.tmp_dir}/images/')
        images = load_files('_static/images/')
        broadcast_message('info', f'Found {len(images)} image(s) in _static/images/.')
        for image in images:
            image = image.lower()
            self._copy_to_tmp(f'_static/images/{image}', 'images/')
            self.images[image] = f'./images/{image}'
            broadcast_message('info', f'Added {image} to build directory and created a URI reference.')

    def _build_styles(self):
        """Copies .css to the temporary folder and builds .sass and .scss to .css to the temp folder.

        Note:
            In case of naming collision between .css and sass, will build sass on top of css. CSS overrules sass.

        Returns:
            None
        """
        force_create_empty_directory(f'{self.tmp_dir}/styles')
        if glob.glob('_static/styles/*.sass') or glob.glob('_static/styles/*.scss'):
            sass.compile(dirname=('static/styles/', f'{self.tmp_dir}/styles/'))
            broadcast_message('info', 'Found and compiled sass files to build directory.')
        for file in os.listdir('_static/styles/'):
            if file.endswith('.css'):
                self._copy_to_tmp(f'_static/styles/{file}', 'styles')
                broadcast_message('info', f'Copied {file} from _static/styles/ to build directory.')

    def _optimize_styles(self):
        """Optimizes the styles in the build directory."""
        shaker = Shaker()
        shaker.discover_add_stylesheets(f'{self.tmp_dir}/styles/', False)
        shaker.discover_add_html(self.tmp_dir, True)
        shaker.optimize(f'{self.tmp_dir}/styles/')
        broadcast_message('info', 'Optimized stylesheets by tree shaking.')

    def _build_markdown(self, file, type_):
        """Builds a .md or .markdown file into a .html file.

        Args:
            file (tuple): Tuple containing the relative path (str) and extension (str) of the file to parse.

        Returns:
            None
        """
        path, extension = file
        broadcast_message('', 'Test')

        with open(f'{self.tmp_dir}/{path}.{extension}') as f:
            data = frontmatter.loads(f.read())

        # Parse markdown to HTML
        html = markdown2.markdown(data.content, extras=["cuddled-lists"]).replace('\n\n', '\n').rstrip()

        # Parse data and add to a page dict
        page = {}
        for key in data.keys():
            page[key] = data[key]

        # Get the template name
        template_name = data.get('template', get_config_value(f'build.templates.{type_}'))
        if template_name == '':
            raise NotImplementedError  # TODO: Implement build error here, because template does not exist.

        # Try to build the page with jinja and markdown
        try:
            template = self.jinja_environment.get_template(f'{template_name}.html')
            with open(f'{self.tmp_dir}/{path}.html', 'w') as f:
                f.writelines(
                    template.render(
                        content=html,
                        site=self.site,
                        page=page,
                        public=get_config_value('public'),
                        images=self.images
                    )
                )
        except TemplateNotFound as e:
            broadcast_message('error', f'Could not build {path}: template {data["template"]} not found.', exc=e)

    def _build_pages(self):
        """Builds all the pages in the /_pages directory.

        Returns:
            None
        """
        for page in os.listdir('_pages/'):
            if page.endswith('.md') or page.endswith('.markdown'):
                self._copy_to_tmp(f'_pages/{page}')
                file = (page.split('.')[0], page.split('.')[1])
                self._build_markdown(file, 'page')

    def _build_posts(self):
        """Builds all posts in the /_posts directory when they should be published.

        This function checks the publication date of a post by checking the first ten characters of the post name.
        Following the format: YYYY-MM-DD-<postname>. If the date has passed or the date is today, the post will be built
        to the output directory, else this will not occur and the post is skipped.

        Returns:
            None
        """
        force_create_empty_directory(f'{self.tmp_dir}/posts')
        for post in os.listdir('_posts/'):
            if post.endswith('.md') or post.endswith('.markdown'):
                try:
                    date = post[:10]
                    if datetime.now() > datetime.strptime(date, '%Y-%m-%d'):
                        self._copy_to_tmp(f'_posts/{post}', 'posts')
                        file = (f'posts/{post.split(".")[0]}', post.split('.')[1])
                        self._build_markdown(file, 'post')
                    else:
                        broadcast_message('warn', f'Skipped building {post} because the date is in the future.')
                except (IndexError, ValueError):
                    broadcast_message('warn', f'Skipped building {post} because of an invalid date pattern.')

    def _clean_tmp(self):
        """Cleans the temporary directory for any remaining artifacts.

        To clean the temporary directory, we will remove all folders that start with an underscore (_), as well as
        all original markdown files (.md / .markdown) in both the original directory, as in the posts directory.

        TODO: Make this more readable, this is a bit cluttered code.
        """
        broadcast_message('info', 'Cleaning out the temporary folder before dispatch.')
        for file in os.listdir(f'{self.tmp_dir}'):
            if os.path.isdir(f'{self.tmp_dir}/{file}') and file.startswith('_'):
                shutil.rmtree(f'{self.tmp_dir}/{file}')
                broadcast_message('info', f'Removed directory: {self.tmp_dir}/{file}.')
            elif file.endswith('.md') or file.endswith('.markdown'):
                os.remove(f'{self.tmp_dir}/{file}')
                broadcast_message('info', f'Removed Markdown page: {self.tmp_dir}/{file}.')
        for file in os.listdir(f'{self.tmp_dir}/posts'):
            if file.endswith('.md') or file.endswith('.markdown'):
                os.remove(f'{self.tmp_dir}/posts/{file}')
                broadcast_message('info', f'Removed Markdown post: {self.tmp_dir}/posts/{file}.')

    def _dispatch_build(self):
        """Safely clears the output directory and dispatches the latest build into this directory.

        Returns:
            None
        """
        force_create_empty_directory('.jackmanbuild')
        broadcast_message('info', 'Done initializing an empty build directory.')

        # Make sure that the output directory actually exists
        with Expects([FileExistsError]):
            os.mkdir('out')

        copy_tree(self.tmp_dir, '.jackmanbuild/')
        broadcast_message('info', 'Dispatched build to build directory.')
        shutil.rmtree('out')
        os.rename('.jackmanbuild/', 'out/')
        shutil.rmtree(self.tmp_dir)
        broadcast_message('info', f'Removed temporary directory: {self.tmp_dir}.')
        broadcast_message('success', 'Build dispatched successfully to output directory.')

    def _create_jinja_env(self):
        """Creates a jinja2 environment with a PackageLoader.

        Returns:
            env (jinja2.Environment): The environment that was configured.

        TODO: Make this configurable.
        """
        env = Environment(
            loader=FileSystemLoader(f'{self.tmp_dir}/_templates'),
        )
        return env

    def _load_templates(self):
        """Loads templates into the temporary template directory.

        Returns:
            None
        """
        broadcast_message('info', 'Loading templates into temporary template directory.')
        start = time.time()
        for file in os.listdir('./_static/templates/'):
            self._copy_to_tmp(f'_static/templates/{file}', '_templates/')
        broadcast_message('echo', f'Done loading templates in {round(time.time() - start, 5)} seconds.')


def main():
    """Main entry point. Sets up the class and builds the entire website to the _website directory
    """
    builder = Builder()
    builder.build()
