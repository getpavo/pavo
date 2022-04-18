import os
import shutil
import time
import glob
from datetime import datetime
from typing import Optional, Union
from distutils.dir_util import copy_tree

import sass
import frontmatter
import yaml
from jinja2 import Environment, FileSystemLoader

from pavo.utils import config, context, files
from pavo.core import messages
from pavo.ddl.build import Post, Page


class WebsiteBuilder:
    """Builder class for Pavo projects. Builds a website from project files.

        Args:
            tmp_dir (str): The location of the temporary directory to write build files to.

        Attributes:
            tmp_dir (str): The location of the temporary directory to write build files to.
            jinja_environment (Environment): The Jinja environment to use when building.
    """

    def __init__(self, tmp_dir: str) -> None:
        self.images: dict[str, str] = {}
        self.data: dict[str, str] = {}
        self.site: dict[str, list[Union[Page, Post]]] = {}

        # Create a temporary folder to write the build to, so we can roll back at any time
        self.tmp_dir: str = tmp_dir
        messages.echo(f'Created temporary directory at {self.tmp_dir}')
        self.jinja_environment: Environment = self._create_jinja_env()

    def build(self, optimize: bool = True) -> None:
        """Public build function. Call to this function builds the project directory to _website.

        Args:
            optimize (bool): Should we optimize images, stylesheets and others. Takes more time, reduces build size.
        """
        self._reset()
        messages.header('Time to build a website!')

        # Load all templates and set up a jinja environment
        self._load_templates()
        self.jinja_environment = self._create_jinja_env()

        # Copy all files from the public folder directly to the build directory
        for file in files.load_files('./_static/public/'):
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

            if optimize:
                # This is temporarily deprecated, will be fixed in a new release
                # TODO: Fix in the Treeshake project.  pylint: disable=fixme
                # self._optimize_styles()
                self._clean_tmp()

        except Exception as err:  # pylint: disable=broad-except
            messages.error(f'Failed to compile: {err.__class__.__name__}. Please see the logs.', err)
            raise err

    def _reset(self) -> None:
        """Resets the builder class to the initial state.
        """
        self.images = {}
        self.data = {}
        site_meta_path = config.get_config_value('build.paths.site_config')
        if not isinstance(site_meta_path, str) \
                or site_meta_path == '' or site_meta_path is None or not os.path.exists(site_meta_path):
            raise FileNotFoundError('Missing website configuration file.')

        with open('./_data/site.yaml', 'r', encoding='utf-8') as file:
            self.site = yaml.safe_load(file)
            self.site['pages'] = []
            self.site['posts'] = []

    def _render(self, render_object: Union[Page, Post],
                template_name: str, rel_path: str) -> None:
        if render_object.content is None:
            raise NotImplementedError

        if render_object.metadata is None:
            raise NotImplementedError

        if template_name == '':
            raise NotImplementedError

        # TODO: Swap this out for .html.jinja, because it is safer.
        template = self.jinja_environment.get_template(f'{template_name}.html')
        with open(f'{self.tmp_dir}/{rel_path}', 'wb') as file:
            file.write(
                template.render(
                    content=render_object.content,
                    site=self.site,
                    data=self.data,
                    page=render_object.metadata,
                    public=config.get_config_value('public'),
                    images=self.images
                ).encode('utf-8')
            )

    def _get_site_data(self) -> None:
        """Retrieves all data from yaml files in ./_data/

        Note:
            This currently checks for both .yaml or .yml files. It is possible that we will move to only supporting
            .yaml in a future release.
        """
        data_files = [
            *glob.glob('./_data/*.yaml'),
            *glob.glob('./_data/*.yml')
        ]

        for file_path in data_files:
            key = os.path.basename(file_path).split('.')[0]
            with open(file_path, 'r', encoding='utf-8') as file:
                if key == 'site':
                    # Since the site data is loaded earlier, there is no reason to make it available as data.
                    continue

                self.data[key] = yaml.safe_load(file)

    def _copy_to_tmp(self, path: str, sub_folder: Optional[str] = None) -> None:
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

    def _build_images(self) -> None:
        """Copies images to the temporary folder.

        TODO: We should add some image optimization in here, because this can be improved by a lot.
        """
        files.force_create_empty_directory(f'{self.tmp_dir}/images/')
        images = files.load_files('_static/images/')
        messages.info(f'Found {len(images)} image(s) in _static/images/.')
        for image in images:
            image = image.lower()
            self._copy_to_tmp(f'_static/images/{image}', 'images/')
            self.images[image] = f'./images/{image}'
            messages.info(f'Added {image} to build directory and created a URI reference.')

    def _build_styles(self) -> None:
        """Copies .css to the temporary folder and builds .sass and .scss to .css to the temp folder.

        Note:
            In case of naming collision between .css and sass, will build sass on top of css. CSS overrules sass.
        """
        files.force_create_empty_directory(f'{self.tmp_dir}/styles')
        if glob.glob('_static/styles/*.sass') or glob.glob('_static/styles/*.scss'):
            sass.compile(dirname=('_static/styles/', f'{self.tmp_dir}/styles/'))
            messages.info('Found and compiled sass files to build directory.')
        for file in os.listdir('_static/styles/'):
            if file.endswith('.css'):
                self._copy_to_tmp(f'_static/styles/{file}', 'styles')
                messages.info(f'Copied {file} from _static/styles/ to build directory.')

    def _discover_pages(self) -> None:
        """Finds all pages that should be built and adds them to the site dictionary.
        """
        for page in os.listdir('_pages/'):
            if page.endswith('.md') or page.endswith('.markdown'):
                self._copy_to_tmp(f'_pages/{page}')

                with open(f'_pages/{page}', encoding='utf-8') as file:
                    data = frontmatter.load(file)

                slug_title = page.split('.')[0]
                self.site['pages'].append(Page(
                    content=files.convert_md_to_html(data.content),
                    metadata=data.metadata,
                    title=data.get('title', slug_title),
                    slug=f'/{slug_title}.html'
                ))

    def _discover_posts(self) -> None:
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

                        with open(f'_posts/{post}', encoding='utf-8') as file:
                            data = frontmatter.load(file)

                        slug_title = post.split(".")[0]
                        self.site['posts'].append(Post(
                            content=files.convert_md_to_html(data.content),
                            metadata=data.metadata,
                            title=data.metadata.get('title', slug_title),
                            slug=f'/posts/{slug_title}.html',
                            date=date.strftime('%B %d, %Y')
                        ))
                except (IndexError, ValueError):
                    messages.warning(f'Skipped indexing post "{post}". Invalid date format. Expected: YYYY-MM-DD.')

        self.site['posts'].sort(key=lambda x: x.title[:10])
        self.site['posts'].reverse()

    def _build_pages(self) -> None:
        """Builds all the pages in the /_pages directory.
        """
        for page in self.site['pages']:
            template = page.metadata.get('template', config.get_config_value('build.default_templates.page'))
            self._render(page, template, page.slug)

    def _build_posts(self) -> None:
        """Builds all posts in the /_posts directory when they should be published.

        This function checks the publication date of a post by checking the first ten characters of the post name.
        Following the format: YYYY-MM-DD-<postname>. If the date has passed or the date is today, the post will be built
        to the output directory, else this will not occur and the post is skipped.
        """
        files.force_create_empty_directory(f'{self.tmp_dir}/posts')
        for post in self.site['posts']:
            template = post.metadata.get('template', config.get_config_value('build.default_templates.post'))
            self._render(post, template, post.slug)

    def _clean_tmp(self) -> None:
        """Cleans the temporary directory for any remaining artifacts.

        To clean the temporary directory, we will remove all folders that start with an underscore (_), as well as
        all original markdown files (.md / .markdown) in both the original directory, as in the posts directory.

        TODO: Make this more readable, this is a bit cluttered code.
        """
        messages.info('Cleaning out the temporary folder before dispatch.')
        for file in os.listdir(f'{self.tmp_dir}'):
            if os.path.isdir(f'{self.tmp_dir}/{file}') and file.startswith('_'):
                shutil.rmtree(f'{self.tmp_dir}/{file}')
                messages.info(f'Removed directory: {self.tmp_dir}/{file}.')
            elif file.endswith('.md') or file.endswith('.markdown'):
                os.remove(f'{self.tmp_dir}/{file}')
                messages.info(f'Removed Markdown page: {self.tmp_dir}/{file}.')
        for file in os.listdir(f'{self.tmp_dir}/posts'):
            if file.endswith('.md') or file.endswith('.markdown'):
                os.remove(f'{self.tmp_dir}/posts/{file}')
                messages.info(f'Removed Markdown post: {self.tmp_dir}/posts/{file}.')

    def dispatch_build(self) -> None:
        """Safely clears the output directory and dispatches the latest build into this directory.
        """
        files.force_create_empty_directory('.pavobuild')
        messages.info('Done initializing an empty build directory.')

        # Make sure that the output directory actually exists
        with context.Expects([FileExistsError]):
            os.mkdir('out')

        copy_tree(self.tmp_dir, '.pavobuild/')
        messages.info('Dispatched build to build directory.')
        shutil.rmtree('out')
        os.rename('.pavobuild/', 'out/')
        messages.success('Build dispatched successfully to output directory.')

    def _create_jinja_env(self) -> Environment:
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
            cache_size=config.get_config_value('build.max_template_cache')
        )

    def _load_templates(self) -> None:
        """Loads templates into the temporary template directory.
        """
        messages.info('Loading templates into temporary template directory.')
        start = time.time()
        for file in os.listdir('./_static/templates/'):
            self._copy_to_tmp(f'_static/templates/{file}', '_templates/')
        messages.echo(f'Done loading templates in {round(time.time() - start, 5)} seconds.')
