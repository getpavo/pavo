import os
import atexit
import tornado.ioloop
import tornado.web
import tornado.autoreload

from typing import Union
from tornado.ioloop import IOLoop

from pavo.core import messages
from .website_builder import WebsiteBuilder


class LocalServer:
    """Containing class for the development server used in Pavo projects.

        Args:
            build_directory (str): The directory to temporarily keep the build in.

        Attributes:
            builder (WebsiteBuilder): The builder that is used to build the website that will be served to the user.
            project_directory (str): The project directory to monitor for changes.
            directory (str): The location of the temporary directory of the builder, used to serve files from.
            paths_to_watch (list): The paths to watch for any changes in files.
            server_settings (dict): Configuration settings that run the httpwatcher server.
            server (HttpWatcherServer): The actual server that does the heavy work, serving content to the user.
        """

    def __init__(self, build_directory: str) -> None:
        self.builder: WebsiteBuilder = WebsiteBuilder(build_directory)
        self.project_directory: str = os.getcwd()
        self.directory: str = self.builder.tmp_dir
        self.paths_to_watch: list[str] = [
            f'{self.project_directory}/_data/',
            f'{self.project_directory}/_pages/',
            f'{self.project_directory}/_posts/',
            f'{self.project_directory}/_static/templates',
            f'{self.project_directory}/_static/styles'
        ]

        self.server_settings: dict[str, Union[str, int]] = {
            'ip': '127.0.0.1',
            'port': 5556
        }

        atexit.register(messages.success, 'Shut down development server.')

        # TODO: Add main entry point that maps to index.html for / route
        self.server: tornado.web.Application = tornado.web.Application([
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': self.directory})
        ])

    def run(self) -> None:
        """Starts a development server and initiates the first build."""
        self.server.listen(self.server_settings['port'], self.server_settings['ip'])
        self.builder.build(False)

        # TODO: Add watchdog daemon that watches file system changes here.

        # TODO: Reload webpage on change detected.
        try:
            messages.success(f'Started local server at {self.server_settings["ip"]}:{self.server_settings["port"]}.')
            tornado.autoreload.start()
            for directory, _, files in os.walk(self.directory):
                [tornado.autoreload.watch(directory + '/' + f) for f in files if not f.startswith('.')]

            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            messages.warning('Detected request to stop server. Please wait.')
            tornado.ioloop.IOLoop.instance().stop()

    def _build_temporary_directory(self) -> None:
        """Triggers a build to the temporary directory on detection of changes to the project."""
        messages.header('Detected changes, rebuilding project.')
        self.builder.build(False)
