"""
The Jackman Command Line Interface is an internal API only. It is not recommended to talk to the CLI directly.
Instead hook onto functions from core and implement your own commands by creating a Python module that registers
entry points for Jackman.

If you wish to communicate using the CLI internal message API, you can hook your function into the broadcast.
Broadcast is a singleton class that should not be instantiated. Instead, you can send a message to the service.
This means that messages sent by Broadcast are not live, instead fetched before and after a function call.

You can find more information about creating plugins and using the public API in the Jackman documentation.
"""

from .broadcast import Broadcast, broadcast_message
