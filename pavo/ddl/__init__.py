"""
The Data Definition Layer (ddl for short) contains dataclasses and abstract base classes for the Pavo ecosystem.
You are free to import these into your own projects, to customize behaviour or to create custom classes.

Note that if you were to import these into your custom files, you should probably import like:
>>> # NOT LIKE THIS:
>>> from pavo.ddl import build
>>> # Preferred like this:
>>> from pavo.ddl import build as models
>>> # Alternatively, if importing multiple different definitions:
>>> from pavo.ddl import (
>>>     build as build_models,
>>>     create as create_models
>>> )
"""
import pavo.ddl._build as build
