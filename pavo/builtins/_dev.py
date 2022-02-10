from typing import Optional
from tempfile import TemporaryDirectory
from dataclasses import dataclass

from pavo.core import messages
from pavo.ddl.commands import CommandInterface
from pavo.server import LocalServer


@dataclass
class Dev(CommandInterface):
    name: str = 'dev'
    help: str = 'Starts a development preview server.'
    allow_outside_project: bool = False

    def run(self, args: Optional[list] = None) -> None:
        with TemporaryDirectory() as tmp_dir:
            server = LocalServer(tmp_dir)
            messages.header('Starting local development server. Awaiting build.')
            server.run()
