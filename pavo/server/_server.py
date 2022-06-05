import os
import atexit
import threading
import asyncio
import webbrowser

import tornado.ioloop
import tornado.web
import tornado.autoreload
import watchdog.observers

from pavo.core import messages
from pavo.core.website_builder import WebsiteBuilder

from ._websocket import RefreshWebSocket
from ._filewatcher import FileWatcher
from ._handler import StaticFileHandler


class LocalServer:
    """Containing class for the development server used in Pavo projects.

    Args:
        build_directory (str): The directory to temporarily keep the build in.

    Attributes:
        builder (WebsiteBuilder): The builder that is used to build the website that will be served to the user.
        project_directory (str): The project directory to monitor for changes.
        directory (str): The location of the temporary directory of the builder, used to serve files from.
        paths_to_watch (set): The paths to watch for any changes in files.
        server (tornado.web.Application): The actual server that does the heavy work, serving content to the user.
    """

    def __init__(self, build_directory: str) -> None:
        self.builder: WebsiteBuilder = WebsiteBuilder(build_directory)
        self.project_directory: str = os.getcwd()
        self.directory: str = self.builder.tmp_dir
        self.paths_to_watch: set[str] = {
            f"{self.project_directory}/_data/",
            f"{self.project_directory}/_pages/",
            f"{self.project_directory}/_posts/",
            f"{self.project_directory}/_static/templates/",
            f"{self.project_directory}/_static/styles/",
        }

        atexit.register(messages.success, "Shut down development server.")

        self.server: tornado.web.Application = tornado.web.Application(
            [
                (r"/ws$", RefreshWebSocket),
                (
                    r"/(.*)$",
                    StaticFileHandler,
                    {"path": self.directory, "default_filename": "index.html"},
                ),
            ]
        )

    def run(self) -> None:
        """Starts a development server and initiates the first build."""
        self.builder.build(False)

        for target in (self._run_tornado, self._run_watcher):
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()

        try:
            while 1:
                # Keep alive
                pass
        except KeyboardInterrupt:
            messages.warning("Detected request to stop server. Please wait.")
            tornado.ioloop.IOLoop().stop()

    def _rebuild_website(self) -> None:
        """Triggers a build to the temporary directory on detection of changes to the project."""
        asyncio.set_event_loop(asyncio.new_event_loop())
        messages.header("Detected changes, rebuilding project.")
        self.builder.build(False)
        asyncio.run(RefreshWebSocket.refresh())

    def _run_tornado(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.server.listen(5556, "127.0.0.1")
        webbrowser.open("http://127.0.0.1:5556")
        tornado.ioloop.IOLoop.current().start()

    def _run_watcher(self):
        observer = watchdog.observers.Observer()
        event_handler = FileWatcher(self._rebuild_website)

        for path in self.paths_to_watch:
            observer.schedule(event_handler, path, True)

        observer.start()
