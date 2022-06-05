import sys
from typing import Optional, Awaitable, Generator

import tornado.web


class StaticFileHandler(tornado.web.StaticFileHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        raise NotImplementedError("Intentionally not implemented")

    def set_extra_headers(self, path: str) -> None:
        # Disallow any form of caching
        self.set_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )
