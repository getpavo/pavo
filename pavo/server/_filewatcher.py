import time
from typing import Callable, Any

import watchdog.events


class FileWatcher(watchdog.events.FileSystemEventHandler):
    """Inherits from watchdog, watches for any event.

    Args:
        callback: The callback function to call on any event.

    Attributes:
        callback: The callback function to call on any event.
        last_handled_event: The float of the time the last event was handled.

    Note:
        Any event fired within a second of the last event will be backed-off and ignored.
        This watcher might need a rework with caching in the future.
    """
    def __init__(self, callback: Callable[[], None]) -> None:
        super().__init__()
        self.callback: Callable[[], None] = callback
        self.last_handled_event: float = time.time()

    def on_any_event(self, event: Any) -> None:
        """
        Catch all event handler.

        Args:
            event: The event that is being caught.
        """
        now = time.time()
        if now - self.last_handled_event < 1:
            return None

        self.last_handled_event = now
        self.callback()
