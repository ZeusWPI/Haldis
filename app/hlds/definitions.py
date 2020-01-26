# Import this class to load the standard HLDS definitions

from os import path
from .parser import parse_all_directory


__all__ = ["location_definitions"]

# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
DATA_DIR = path.join(path.dirname(__file__), "..", "..", "data")

# pylint: disable=invalid-name
location_definitions = parse_all_directory(DATA_DIR)
