import logging
from typing import Any, Type

import colorama

from pavo.ddl import messages, log
from pavo.utils import config
from pavo.core.exceptions import MessageTypeAlreadyExists


class MessageHandler(messages.MessageHandlerInterface):
    def __init__(self) -> None:
        colorama.init()
        self.logger = logging.getLogger('pavo')
        self._setup_logging()

        self.registered_types: dict[str, Type[messages.MessageInterface]] = {}
        self.register(messages.AskMessage)
        self.register(messages.DebugMessage)
        self.register(messages.EchoMessage)
        self.register(messages.InfoMessage)
        self.register(messages.WarnMessage)
        self.register(messages.ErrorMessage)
        self.register(messages.SuccessMessage)

    def _setup_logging(self) -> None:
        """Sets up the logging functionality in the MessageHandler."""
        log_level = 20
        try:
            log_level = config.get_config_value('logging.level')
            self.logger.disabled = config.get_config_value('logging.enabled') == 'false'

            # Only add a file formatter when the configuration file can be found
            # This ensures that no log file exists outside a Pavo project
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler = logging.FileHandler('pavo.log', delay=True)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            self.logger.propagate = False
        except FileNotFoundError:
            self.logger.disabled = True
        finally:
            self.logger.setLevel(log_level if isinstance(log_level, (int, str)) else 20)

    def print(self, message_type: str, msg: str, **kwargs: Any) -> bool:
        """Handles a message using the specified registered message type.

            Args:
                message_type (str): The type of the message to use.
                msg (str): The message to send.
                **kwargs: Optional arguments to send to the message handler function.

            Returns:
                bool: Whether the message was sent to the user without warning.
        """
        try:
            class_object = self.registered_types[message_type]
            cls = class_object()
            cls.print(msg, **kwargs)

            # For some message types, we should skip logging.
            if cls.log_level == log.LogLevels.NOTSET or kwargs.get('disable_logging', False):
                return True

            # Log the message
            if 'logger_name' in kwargs:
                alt = logging.getLogger(kwargs['logger_name'])
                alt.log(cls.log_level.value, msg)
            else:
                self.logger.log(cls.log_level.value, msg)

            return True
        except KeyError:
            self.print('error', f'A message with an unregistered message type was caught: {message_type}.')
            self.print('echo', f'Message content: {msg}')
            return False
        except Exception as err:  # pylint: disable=broad-except
            self.print('error', f'Error when trying to send a message: {repr(err)}')
            self.print('debug', f'Caught a message that caused an error: {msg}')
            return False

    def register(self, message_interface: Type[messages.MessageInterface]) -> bool:
        """Registers custom message types to be used when sending a message.

            Args:
                message_interface (MessageInterface): The class that implements the MessageInterface.

            Returns:
                bool: Whether the registration has succeeded.
        """
        name = message_interface.name
        if self.registered_types.get(name) is not None:
            raise MessageTypeAlreadyExists(name)

        self.registered_types[name] = message_interface
        return True
