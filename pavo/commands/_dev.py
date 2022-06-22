from typing import Optional
from tempfile import TemporaryDirectory
from dataclasses import dataclass
import argparse

from pavo.core import messages
from pavo.ddl.commands import CommandInterface
from pavo.server import LocalServer


@dataclass
class Dev(CommandInterface):
    """Built-in 'dev' command."""

    name: str = "dev"
    help: str = "Starts a development preview server."
    allow_outside_project: bool = False

    def run(self, args: argparse.Namespace) -> None:
        """Starts a development server and builds the website to a temporary directory.

        Args:
            args: The arguments provided by the caller.
        """
        with TemporaryDirectory() as tmp_dir:
            server = LocalServer(tmp_dir)
            messages.header("Starting local development server. Awaiting build.")
            server.run()

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        return
