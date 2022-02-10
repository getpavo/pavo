from typing import Union, Optional, Awaitable

import tornado.websocket

from pavo.core import messages


class RefreshWebSocket(tornado.websocket.WebSocketHandler):
    live_connections: set[tornado.websocket.WebSocketHandler] = set()

    def open(self, *args: str, **kwargs: str) -> Optional[Awaitable[None]]:
        self.live_connections.add(self)
        messages.debug(f'Opened a websocket from IP: {self.request.remote_ip}')
        return None  # pylint: disable=useless-return

    def on_message(self, message: Union[str, bytes]) -> Optional[Awaitable[None]]:
        pass

    def on_close(self) -> None:
        self.live_connections.remove(self)
        messages.debug(f'Closed a websocket from IP: {self.request.remote_ip}')

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    @classmethod
    async def refresh(cls) -> None:
        print(cls.live_connections)
        for connection in cls.live_connections:
            if not connection.ws_connection or not connection.ws_connection.stream.socket:
                cls.live_connections.remove(connection)
            else:
                await connection.write_message('Detected changes, refresh the page.')
