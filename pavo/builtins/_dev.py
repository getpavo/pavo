from typing import Optional
from tempfile import TemporaryDirectory
from dataclasses import dataclass

from pavo.core import messages, LocalServer
from pavo.ddl.commands import CommandInterface


@dataclass
class Dev(CommandInterface):
    name: str = 'dev'
    help: str = 'Starts the development preview server.'
    allow_outside_project: bool = False

    def run(self, args: Optional[list] = None) -> None:
        with TemporaryDirectory() as tmp_dir:
            server = LocalServer(tmp_dir)
            messages.header('Starting local development server. Awaiting build.')
            server.run()
