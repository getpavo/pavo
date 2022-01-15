from enum import Enum


class LogLevels(Enum):
    """Enum that contains the different levels of logging."""
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0
