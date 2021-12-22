"""
[WIP] Plugin ecosystem for Pavo.

The idea is that Pavo supports two types of plugins:
    1. Modules for Pavo, that register commands / actions using the hooks and other functions.
    2. Scripts that are implemented in the /scripts/ directory of an active project.
"""
from .hooks import global_hook_manager, HookManager, register_hook
