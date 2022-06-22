import argparse

from dataclasses import dataclass
from typing import Optional
from tempfile import TemporaryDirectory

from pavo.ddl.commands import CommandInterface
from pavo.core import WebsiteBuilder


@dataclass
class Build(CommandInterface):
    """Built-in 'build' command."""

    name: str = "build"
    help: str = "Builds and optimizes the website in the output directory."
    allow_outside_project: bool = False

    def run(self, args: argparse.Namespace) -> None:
        """Creates a temporary directory, builds the website and dispatches it.

        Args:
            args: The arguments provided by the caller.
        """
        with TemporaryDirectory() as build_directory:
            builder = WebsiteBuilder(build_directory)
            builder.build()
            builder.dispatch_build()

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        return
