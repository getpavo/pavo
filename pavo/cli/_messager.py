from typing import Callable, Optional, Any, Type

import pavo.cli._messages as default_messages
from pavo.ddl import messages
from ._errors import MessageHandlerAlreadyExists


message_types: dict[str, Type[messages.MessageInterface]] = {
    'ask': messages.AskMessage,
    'debug': messages.DebugMessage,
    'echo': messages.EchoMessage,
    'info': messages.InfoMessage,
    'warn': messages.WarnMessage,
    'error': messages.ErrorMessage,
    'success': messages.SuccessMessage
}


def handle_message(handler: str, msg: str, **kwargs: Any) -> bool:
    """Handles a message using the specified handler function.
    Args:
        handler (str): The type of the message to use.
        msg (str): The message to send.
        **kwargs: Optional arguments to send to the message handler function.

    Returns:
        bool: Whether the message was sent to the user without warning.
    """
    try:
        message = message_types[handler]()
        print(message.as_formatted_string(msg, **kwargs))
        return True
    except Exception as err:  # pylint: disable=broad-except
        message_types['error']().as_formatted_string(f'Error when trying to send a message: {repr(err)}', exc=err)
        message_types['debug']().as_formatted_string(f'Caught a message that caused an error: {msg}')
        return False


def register_custom_message_handler(message_interface: Type[messages.MessageInterface]) -> bool:
    """Registers custom message types to be used when sending a message.

    Args:
        message_interface (MessageInterface): The function that handles the message being parsed.

    Returns:
        bool: Whether the registration has succeeded.
    """
    name = message_interface.name
    if message_types.get(name) is not None:
        # Cannot overwrite existing custom message type.
        raise MessageHandlerAlreadyExists

    message_types[name] = message_interface
    return True
