from dataclasses import dataclass
from typing import Optional
from tempfile import TemporaryDirectory

from pavo.ddl.commands import CommandInterface
from pavo.core import WebsiteBuilder


@dataclass
class Build(CommandInterface):
    name: str = 'build'
    help: str = 'Builds and optimizes the website in the output directory.'
    allow_outside_project: bool = False

    def run(self, args: Optional[list] = None) -> None:
        """Builds the website to the output directory."""
        with TemporaryDirectory() as build_directory:
            builder = WebsiteBuilder(build_directory)
            builder.build()
            builder.dispatch_build()
