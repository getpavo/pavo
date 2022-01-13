"""
The Pavo Command Line Interface is an internal API only. It is not recommended talking to the CLI directly.
Instead, hook onto functions from core and implement your own commands by creating a Python module that registers
entry points for Pavo.

You can find more information about creating plugins and using the public API in the Pavo documentation.
"""
import pavo.cli._errors as errors
from ._messager import handle_message, register_custom_message_handler
