import time
from typing import Callable

import watchdog.events


class FileWatcher(watchdog.events.FileSystemEventHandler):
    def __init__(self, callback: Callable[[], None]) -> None:
        super().__init__()
        self.callback: Callable[[], None] = callback
        self.last_handled_event: float = time.time()

    def on_any_event(self, event):
        now = time.time()
        if now - self.last_handled_event < 1:
            return

        self.last_handled_event = now
        self.callback()
