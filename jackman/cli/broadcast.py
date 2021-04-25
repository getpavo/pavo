from ._messages import debug, echo, info, warn, error
from jackman.helpers.decorators import singleton


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
    def __init__(self):
        self._broadcast_types = {
            'debug': debug,
            'echo': echo,
            'info': info,
            'warn': warn,
            'error': error,
        }
        self._unheard_messages = []

    def send(self, type_, message, exc=None):
        """Queues a message to be listened at by the listener.

        Note:
            It is recommended to use the shorthand function for sending a message: broadcast_message().

        Args:
            type_ (str): The type of message to be sent.
            message (str): The message to be sent.
            exc (Exception): The exception that was raised in case of an error.

        Returns:
            bool: Whether or not the message was queued successfully.
        """
        if type_ in self._broadcast_types:
            if exc is None:
                self._unheard_messages.append({
                    'type': type_,
                    'message': message
                })
                return True
            elif exc is not None and type_ == 'error':
                self._unheard_messages.append({
                    'type': type_,
                    'message': message,
                    'exception': exc
                })
                return True

        return False

    def listen(self):
        """Listens to the message that has been waiting in queue the longest and removes it when listened to.

        Returns:
            bool: Whether or not the message was successfully listened to.
        """
        if len(self._unheard_messages) == 0:
            return True

        entry = self._unheard_messages[0]
        try:
            if entry['type'] == 'error':
                self._broadcast_types.get(entry['type'])(entry['message'], entry['exception'])
            else:
                self._broadcast_types.get(entry['type'])(entry['message'])
            del(self._unheard_messages[0])
            return True
        except Exception as e:
            self.send('error', f'Error when trying to send via Broadcast: {repr(e)}', e)
            return False

    def listen_all(self):
        """Listens to all currently queued messages in order of queueing."""
        for i in range(len(self._unheard_messages)):
            self.listen()

    def spy(self):
        """Returns all unheard messages without deleting them."""
        return self._unheard_messages


def broadcast_message(type_, message, exc=None):
    """Shorthand function for Broadcast().send()

    Args:
        type_ (str): The type of message to be sent.
        message (str): The message to be sent.
        exc (Exception): The exception that was raised in case of an error.

    Returns:
        bool: Whether or not the message was queued successfully.
    """
    broadcast = Broadcast()
    return broadcast.send(type_, message, exc)
