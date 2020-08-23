import os
import sass
import shutil
import time
import glob
import frontmatter
import markdown2
import jinja2

from distutils.dir_util import copy_tree


class Builder:
    """
    Builder class for Jackman projects. Literally builds a website from jackman-files.
    """
    def __init__(self):
        # Create a temporary folder to write the build to, so we can rollback at any time
        self.tmp_dir = f'_tmp_{int(time.time())}'
        os.mkdir(self.tmp_dir, 0o755)

        self.__build_pages()
        self.__build_posts()
        self.__build_styles()
        self.__clean_tmp()
        self.__dispatch_build()

    def __copy_to_tmp(self, path, sub_folder=''):
        """
        Copies a file to the temporary working directory.

        Parameters
        ----------
        path : str
            The relative path to the file to copy.
        sub_folder : str
            The directory in the temp directory to copy the file to. Defaults to ''.

        Returns
        -------
        None
        """
        shutil.copy(path, f'{self.tmp_dir}/{sub_folder}')

    def __build_styles(self):
        """
        Copies .css to the temporary folder and builds .sass and .scss to .css to the temp folder.

        Notes
        -----
        In case of naming collision between .css and sass, will build sass on top of css. CSS overrules sass.

        Returns
        -------
        None
        """
        os.mkdir(f'{self.tmp_dir}/styles')
        if glob.glob('_static/styles/*.sass') or glob.glob('_static/styles/*.scss'):
            sass.compile(dirname=('static/styles/', f'{self.tmp_dir}/styles/'))
        for file in os.listdir('_static/styles/'):
            if file.endswith('.css'):
                self.__copy_to_tmp(f'_static/styles/{file}', 'styles')

    def __build_html(self, file):
        """
        Builds a .md or .markdown file into a functioning .html file.

        Parameters
        ----------
        file : tuple
            Tuple containing the relative path and extension of the file to parse.

        Returns
        -------
        None
        """
        path, extension = file
        with open(f'{self.tmp_dir}/{path}.{extension}') as f:
            data = frontmatter.loads(f.read())

        # Parse markdown to HTML
        html = markdown2.markdown(data.content, extras=["cuddled-lists"]).replace('\n\n', '\n').rstrip()

        # Add metadata into HTML
        # TODO: Make this work with template variables e.q. {{meta}} to include meta
        for key in data.metadata:
            page_template = data.metadata[key] if key == 'template' else None

        # TODO: Implement template functionality

        with open(f'{self.tmp_dir}/{name}.html', 'w') as f:
            f.writelines(html)

    def __build_from_template(self, template):
        pass

    def __build_pages(self):
        """
        Builds all the pages in the /_pages directory.

        Returns
        -------
        None
        """
        for page in os.listdir('_pages/'):
            if page.endswith('.md') or page.endswith('.markdown'):
                self.__copy_to_tmp(f'_pages/{page}')
                file = (page.split('.')[0], page.split('.')[1])
                self.__build_html(file)

    def __build_posts(self):
        os.mkdir(f'{self.tmp_dir}/posts')

    def __clean_tmp(self):
        """
        Cleans the temporary directory for any remaining artifacts.

        Returns
        -------
        None
        """
        for file in os.listdir(f'{self.tmp_dir}'):
            if file.endswith('.md') or file.endswith('.markdown'):
                os.remove(f'{self.tmp_dir}/{file}')

    def __dispatch_build(self):
        """
        Clears the _website directory and dispatches the latest build into this directory.

        Returns
        -------
        None
        """
        shutil.rmtree('_website')
        os.mkdir('_website')
        copy_tree(self.tmp_dir, '_website')
        shutil.rmtree(self.tmp_dir)
