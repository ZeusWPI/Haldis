# Import this class to load the standard HLDS definitions

from os import path
from typing import List
from .parser import parse_all_directory
from .models import Location


__all__ = ["location_definitions"]

# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
DATA_DIR = path.join(path.dirname(__file__), "..", "..", "data")

# pylint: disable=invalid-name
location_definitions: List[Location] = parse_all_directory(DATA_DIR)
location_definitions.sort(key=lambda l: l.name)
