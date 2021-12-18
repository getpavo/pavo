"""
The Pavo Command Line Interface is an internal API only. It is not recommended talking to the CLI directly.
Instead, hook onto functions from core and implement your own commands by creating a Python module that registers
entry points for Pavo.

If you wish to communicate using the CLI internal message API, you can hook your function into the broadcast.
Broadcast is a singleton class that should not be instantiated. Instead, you can send a message to the service.
This means that messages sent by Broadcast are not live, instead fetched before and after a function call.

You can find more information about creating plugins and using the public API in the Pavo documentation.
"""
from ._messager import handle_message, register_custom_message_handler
import pavo.cli._errors as errors
