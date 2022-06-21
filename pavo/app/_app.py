import argparse
import pkg_resources

from pavo.ddl.commands import CommandInterface
from pavo.core import CommandManager
from pavo.commands import Build, Create, Dev, Help


command_manager = CommandManager()
command_manager.register(Build())
command_manager.register(Create())
command_manager.register(Dev())
command_manager.register(Help(command_manager=command_manager))
