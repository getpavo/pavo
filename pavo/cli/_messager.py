from typing import Callable, Optional, Any

import pavo.cli._messages as default_messages
from ._errors import MessageHandlerAlreadyExists


message_types: dict[str, Callable[..., Optional[str]]] = {
    'ask': default_messages.ask,
    'debug': default_messages.debug,
    'echo': default_messages.echo,
    'info': default_messages.info,
    'warn': default_messages.warn,
    'error': default_messages.error,
    'success': default_messages.success
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
        message_types[handler](msg, **kwargs)
        return True
    except Exception as err:  # pylint: disable=broad-except
        message_types['error'](f'Error when trying to send a message: {repr(err)}', exc=err, unsafe=True)
        message_types['debug'](f'Caught a message that caused an error: {msg}')
        return False


def register_custom_message_handler(name: str, func: Callable[..., Optional[str]]) -> bool:
    """Registers custom message types to be used when sending a message.

    Args:
        name (str): The name of the type to register.
        func (Callable): The function that handles the message being parsed.

    Returns:
        bool: Whether the registration has succeeded.
    """
    if message_types.get(name) is not None:
        # Cannot overwrite existing custom message type.
        raise MessageHandlerAlreadyExists

    message_types[name] = func
    return True
