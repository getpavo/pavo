"""
The Pavo Command Line Interface is an internal API only. It is not recommended talking to the CLI directly.
Instead, hook onto functions from core and implement your own commands by creating a Python module that registers
entry points for Pavo.

You can find more information about creating plugins and using the public API in the Pavo documentation.
"""
from pavo.app._cli import PavoApp
import pavo.app._errors as errors
