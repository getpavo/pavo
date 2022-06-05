from typing import Optional, Awaitable, Generator

import tornado.web


class StaticFileHandler(tornado.web.StaticFileHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_extra_headers(self, path: str) -> None:
        self.set_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )

    def get_content(
        self, abspath: str, start: Optional[int] = None, end: Optional[int] = None
    ) -> Generator[bytes, None, None]:
        websocket_script_injection = """<script type="application/javascript" src="/websocket.js"></script>
        </body>
        """.encode(
            "utf-8"
        )

        # TODO: Fix content-length error when retrieving file
        if self.get_content_type() == "text/html":
            with open(abspath, "rb") as file:
                yield file.read().replace(b"</body>", websocket_script_injection)
