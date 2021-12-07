from threading import Thread
from typing import Callable, Any

from ._messages import debug, echo, info, warn, error, success
from pavo.helpers.decorators import singleton


@singleton
class Broadcast(object):
    """Singleton Broadcast class that holds all sent messages in memory.

    The Broadcast functionality works with sending and listening. When listening, a message is removed from
    the queue. When sending, a message is added. With the introduction of multithreading in our program,
    broadcasting to the CLI is live and almost instant.

    Attributes:
        _broadcast_types (dict): A dictionary with all available message types.
        _unheard_messages (list): A list of all messages that have not been listened to.
    """
    def __init__(self) -> None:
        self._broadcast_types: dict[str, Callable] = {
            'debug': debug,
            'echo': echo,
            'info': info,
            'warn': warn,
            'error': error,
            'success': success
        }
        self._unheard_messages: list[dict[str, Any]] = []

    def send(self, type_: str, message: str, **kwargs: Any) -> bool:
        """Queues a message to be listened at by the listener.

        Note:
            It is recommended to use the shorthand function for sending a message: broadcast_message().

        Args:
            type_ (str): The type of message to be sent.
            message (str): The message to be sent.
            kwargs: A list of keyword arguments based on the type of message you are sending.

        Returns:
            bool: Whether the message was queued successfully.
        """
        if type_ in self._broadcast_types:
            self._unheard_messages.append({
                'type': type_,
                'message': message,
                'kwargs': kwargs
            })
            return True

        return False

    def listen(self) -> bool:
        """Listens to the message that has been waiting in queue the longest and removes it when listened to.

        Returns:
            bool: Whether the message was successfully listened to.
        """
        if len(self._unheard_messages) == 0:
            return True

        entry = self._unheard_messages[0]
        try:
            if 'exc' in entry['kwargs'] and entry['kwargs']['exc'] is not None:
                exc = entry['kwargs']['exc']
                del(entry['kwargs']['exc'])
                self._broadcast_types['error'](entry['message'], exc=exc, **entry['kwargs'])
            else:
                self._broadcast_types[entry['type']](entry['message'], **entry['kwargs'])
            del(self._unheard_messages[0])
            return True
        except Exception as e:
            self.send('error', f'Error when trying to listen to a message via Broadcast: {repr(e)}', exc=e, unsafe=True)
            self.send('debug', f'Caught a message that caused an error: {self._unheard_messages[0]}')
            del(self._unheard_messages[0])
            return False

    def listen_all(self) -> None:
        """Listens to all currently queued messages in order of queueing."""
        for i in range(len(self._unheard_messages)):
            self.listen()

    def _listen_looped(self) -> None:
        """Infinite loop to listen to all incoming messages.

        Note:
            This function is only used and called by the multi-threaded subscribers, in order to acquire live data.
        """
        while True:
            self.listen_all()

    def spy(self) -> list[dict[str, Any]]:
        """Returns all unheard messages without deleting them."""
        return self._unheard_messages

    def subscribe(self) -> Thread:
        """Creates a listener daemon thread that enables listening to broadcast communication.

        Returns:
            Thread: The thread with a looped listened function attached.
        """
        listener = Thread(target=self._listen_looped)
        listener.daemon = True
        return listener


def broadcast_message(type_: str, message: str, **kwargs: Any) -> bool:
    """Shorthand function for Broadcast().send()

    Args:
        type_ (str): The type of message to be sent.
        message (str): The message to be sent.
        kwargs: A list of keyword arguments based on the type of message you are sending.

    Returns:
        bool: Whether the message was queued successfully.
    """
    broadcast = Broadcast()
    return broadcast.send(type_, message, **kwargs)
