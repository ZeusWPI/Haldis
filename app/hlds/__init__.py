"""
If you want to access the definitions, then just do
>>> from hlds.definitions import location_definitions

These are not imported in this module's init, to avoid opening the definition files and running the
parser on them when testing other code in this module, or when testing the parser on other files.
"""

from .models import Location, Choice, Option
