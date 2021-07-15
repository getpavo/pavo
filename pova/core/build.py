import os
import shutil
import time
import glob
from datetime import datetime

import sass
import frontmatter
import markdown2
import yaml

from jinja2 import Environment, FileSystemLoader
from distutils.dir_util import copy_tree
from treeshake import Shaker

from pova.cli import broadcast_message
from pova.helpers.context import Expects
from pova.helpers.files import load_files, set_dir, cd_is_project, force_create_empty_directory
from pova.helpers.config import get_config_value


class Builder:
    """Builder class for Pova projects. Builds a website from project files.

    Args:
        mode (str): Type of build. Defaults to 'production' - which dispatches the build to _website directory.

    Attributes:
        mode (str): Type of build. Defaults to 'production' - which dispatches the build to _website directory.
        tmp_dir (str): Path to the temporary directory used for building before dispatching.
        jinja_environment (jinja2.environment): The Jinja environment to use when building.
    """

    def __init__(self, mode="production"):
        self.mode = mode
        self.directory = os.getcwd() if cd_is_project() else None

        # Create a temporary folder to write the build to, so we can rollback at any time
        self.tmp_dir = f'_tmp_{int(time.time())}'
        os.mkdir(self.tmp_dir, 0o755)
        broadcast_message('echo', f'Created temporary directory with name {self.tmp_dir}')
        self.jinja_environment: Environment = self._create_jinja_env()

    def build(self):
        """Public build function. Call to this function builds the project directory to _website.
        """
        self._reset()
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
        try:
            self._get_site_data()
            self._discover_pages()
            self._discover_posts()
            self._build_images()
            self._build_pages()
            self._build_posts()
            self._build_styles()

            if self.mode not in ['development', 'dev']:
                self._optimize_styles()
                self._clean_tmp()
                self._dispatch_build()

        except Exception as e:
            broadcast_message('error', f'Failed to compile: {e.__class__.__name__}. Please refer to the logs.', exc=e)
            shutil.rmtree(self.tmp_dir)
            exit()

    def _reset(self):
        """Resets the builder class to the initial state.
        """
        self.images = {}
        self.data = {}
        site_meta_path = get_config_value('build.paths.site_config')
        if site_meta_path == '' or site_meta_path is None or not os.path.exists(site_meta_path):
            raise FileNotFoundError('Missing website configuration file.')

        with open(f'./_data/site.yaml', 'r') as f:
            self.site = yaml.safe_load(f)
            self.site['pages'] = []
            self.site['posts'] = []

    def _render(self, render_object, template_name, rel_path):
        if 'content' not in render_object.keys():
            raise NotImplementedError

        if 'metadata' not in render_object.keys():
            raise NotImplementedError

        if template_name == '':
            raise NotImplementedError

        template = self.jinja_environment.get_template(f'{template_name}.html')
        with open(f'{self.tmp_dir}/{rel_path}', 'w') as f:
            f.writelines(
                template.render(
                    content=render_object['content'],
                    site=self.site,
                    data=self.data,
                    page=render_object['metadata'],
                    public=get_config_value('public'),
                    images=self.images
                )
            )

    @staticmethod
    def _build_markdown(markdown):
        """Translates raw markdown into ready html code.

        This method uses the markdown build configuration value in the .povaconfig file, which tells this method
        what extras to use when building. (Default: fenced code blocks and cuddled lists)

        Args:
            markdown (str): The Markdown code to be translated to HTML.

        Returns:
            str: The html that was built from the markdown.
        """
        html = markdown2.markdown(markdown, extras=get_config_value('build.markdown.extras'))
        html = html.replace('\n\n', '\n').rstrip()

        return html

    def _get_site_data(self):
        """Retrieves all data from yaml files in ./_data/
        """
        data_files = []
        for file in glob.glob('./_data/*.yaml'):
            data_files.append(file)

        for file in data_files:
            key = os.path.basename(file).split('.')[0]
            with open(file, 'r') as f:
                if key == 'site':
                    continue

                self.data[key] = yaml.safe_load(f)

    def _copy_to_tmp(self, path, sub_folder=None):
        """Copies a file to the temporary working directory.

        Args:
            path (str): The relative path to the file to copy.
            sub_folder (str): The directory in the temporary directory to copy the file to. Defaults to ''.
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
        """
        force_create_empty_directory(f'{self.tmp_dir}/styles')
        if glob.glob('_static/styles/*.sass') or glob.glob('_static/styles/*.scss'):
            sass.compile(dirname=('_static/styles/', f'{self.tmp_dir}/styles/'))
            broadcast_message('info', 'Found and compiled sass files to build directory.')
        for file in os.listdir('_static/styles/'):
            if file.endswith('.css'):
                self._copy_to_tmp(f'_static/styles/{file}', 'styles')
                broadcast_message('info', f'Copied {file} from _static/styles/ to build directory.')

    def _optimize_styles(self):
        """Optimizes the styles in the build directory.

        Note:
            Because Treeshake checks whether or not files include references to other files, it is necessary to first
            get all styles into the /styles/ directory, after which optimization takes place. Because optimization does
            overwrite used files, but does not remove unused files, we need to write to a new directory and replace the
            styles directory with this new directory.
        """
        force_create_empty_directory(f'{self.tmp_dir}/optimized_styles')
        shaker = Shaker()
        shaker.discover_add_stylesheets(f'{self.tmp_dir}/styles/', False)
        shaker.discover_add_html(self.tmp_dir, True)
        shaker.optimize(f'{self.tmp_dir}/optimized_styles/')
        shutil.rmtree(f'{self.tmp_dir}/styles/')
        shutil.copytree(f'{self.tmp_dir}/optimized_styles/', f'{self.tmp_dir}/styles/')
        shutil.rmtree(f'{self.tmp_dir}/optimized_styles/')
        broadcast_message('info', 'Optimized stylesheets by tree shaking.')

    def _discover_pages(self):
        """Finds all pages that should be built and adds them to the site dictionary.
        """
        for page in os.listdir('_pages/'):
            if page.endswith('.md') or page.endswith('.markdown'):
                self._copy_to_tmp(f'_pages/{page}')

                with open(f'_pages/{page}') as f:
                    data = frontmatter.load(f)

                slug_title = page.split('.')[0]
                self.site['pages'].append({
                    'slug': f'/{slug_title}.html',
                    'title': data.get('title', slug_title),
                    'content': self._build_markdown(data.content),
                    'metadata': data.metadata
                })

    def _discover_posts(self):
        """Finds all posts that should be built and adds them to the site dictionary.

        This method filters all posts that have an invalid date or which date has not yet passed.
        This way, the posts that are not ready yet, are not built and therefore not visible to visitors.
        """
        for post in os.listdir('_posts/'):
            if post.endswith('.md') or post.endswith('.markdown'):
                try:
                    date = datetime.strptime(post[:10], '%Y-%m-%d')
                    if datetime.now() > date:
                        self._copy_to_tmp(f'_posts/{post}', 'posts')

                        with open(f'_posts/{post}') as f:
                            data = frontmatter.load(f)

                        slug_title = post.split(".")[0]
                        self.site['posts'].append({
                            'slug': f'/posts/{slug_title}.html',
                            'title': data.metadata.get('title', slug_title),
                            'content': self._build_markdown(data.content),
                            'metadata': data.metadata,
                            'date': date.strftime('%B %d, %Y'),
                        })
                except (IndexError, ValueError):
                    broadcast_message('warn', f'Skipped indexing post "{post}". Invalid date format.')

        self.site['posts'].sort(key=lambda x: x['title'][:10])
        self.site['posts'].reverse()

    def _build_pages(self):
        """Builds all the pages in the /_pages directory.
        """
        for page in self.site['pages']:
            template = page['metadata'].get('template', get_config_value('build.default_templates.page'))
            self._render(page, template, page['slug'])

    def _build_posts(self):
        """Builds all posts in the /_posts directory when they should be published.

        This function checks the publication date of a post by checking the first ten characters of the post name.
        Following the format: YYYY-MM-DD-<postname>. If the date has passed or the date is today, the post will be built
        to the output directory, else this will not occur and the post is skipped.
        """
        force_create_empty_directory(f'{self.tmp_dir}/posts')
        for post in self.site['posts']:
            template = post['metadata'].get('template', get_config_value('build.default_templates.post'))
            self._render(post, template, post['slug'])

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
        """
        force_create_empty_directory('.povabuild')
        broadcast_message('info', 'Done initializing an empty build directory.')

        # Make sure that the output directory actually exists
        with Expects([FileExistsError]):
            os.mkdir('out')

        copy_tree(self.tmp_dir, '.povabuild/')
        broadcast_message('info', 'Dispatched build to build directory.')
        shutil.rmtree('out')
        os.rename('.povabuild/', 'out/')
        shutil.rmtree(self.tmp_dir)
        broadcast_message('info', f'Removed temporary directory: {self.tmp_dir}.')
        broadcast_message('success', 'Build dispatched successfully to output directory.')

    def _create_jinja_env(self):
        """Creates a jinja2 environment with a PackageLoader.

        Returns:
            Environment: The environment that was configured.
        """
        return Environment(
            loader=FileSystemLoader(f'{self.tmp_dir}/_templates'),
            line_statement_prefix='>>',
            line_comment_prefix='#',
            trim_blocks=True,
            lstrip_blocks=True,
            cache_size=get_config_value('build.max_template_cache')
        )

    def _load_templates(self):
        """Loads templates into the temporary template directory.
        """
        broadcast_message('info', 'Loading templates into temporary template directory.')
        start = time.time()
        for file in os.listdir('./_static/templates/'):
            self._copy_to_tmp(f'_static/templates/{file}', '_templates/')
        broadcast_message('echo', f'Done loading templates in {round(time.time() - start, 5)} seconds.')


def main():
    """Builds the website to the output directory.
    """
    builder = Builder()
    builder.build()
