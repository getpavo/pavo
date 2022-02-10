from typing import Optional, Awaitable

import tornado.web


class StaticFileHandler(tornado.web.StaticFileHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_extra_headers(self, path: str) -> None:
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
