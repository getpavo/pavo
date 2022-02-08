"""
The Data Definition Layer (ddl for short) contains dataclasses and abstract base classes for the Pavo ecosystem.
You are free to import these into your own projects, to customize behaviour or to create custom classes.

Note that if you were to import these into your custom files, you should probably import like:
>>> # Probably never like this, because the namespace might interfere with methods / classes:
>>> from pavo.ddl import build
>>> # For the love of God, please don't wildcard import:
>>> from pavo.ddl.build import *
>>> # We prefer importing like this, because it adheres to the other Pavo importing:
>>> from pavo.ddl import build as models
>>> # Alternatively, if importing multiple different definitions:
>>> from pavo.ddl import (
>>>     build as build_models,
>>>     create as create_models
>>> )
>>> # Finally, you can also import models on a per-model basis:
>>> from pavo.ddl.build import Post, Page
"""
from pavo.ddl import build
from pavo.ddl import hooks
from pavo.ddl import commands
from pavo.ddl import plugins
