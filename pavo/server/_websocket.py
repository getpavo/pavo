from typing import Union, Optional, Awaitable

import tornado.websocket

from pavo.core import messages


class RefreshWebSocket(tornado.websocket.WebSocketHandler):
    """The Websocket connection that sends a signal to refresh on file update."""

    live_connections: set[tornado.websocket.WebSocketHandler] = set()

    def open(self, *args: str, **kwargs: str) -> Optional[Awaitable[None]]:
        """On opening the connection, add it to the live connections and log it."""
        self.live_connections.add(self)
        messages.debug(f"Opened a websocket from IP: {self.request.remote_ip}")
        return None  # pylint:disable=useless-return

    def on_message(self, message: Union[str, bytes]) -> Optional[Awaitable[None]]:
        """On receiving a message, do nothing."""

    def on_close(self) -> None:
        """On closing the connection, remove it from the live connections."""
        self.live_connections.remove(self)
        messages.debug(f"Closed a websocket from IP: {self.request.remote_ip}")

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        """On receiving data over the connection, do nothing."""

    @classmethod
    async def refresh(cls) -> None:
        """Sends a signal to the Websocket client to refresh the page."""
        for connection in cls.live_connections:
            if (
                not connection.ws_connection
                or not connection.ws_connection.stream
                or not connection.ws_connection.stream.socket
            ):
                cls.live_connections.remove(connection)
            else:
                await connection.write_message("Detected changes, refresh the page.")
