# Import this class to load the standard HLDS definitions

from os import path
import itertools
from .parser import parse_all_directory


__all__ = ["definitions"]

# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
data_dir = path.join(path.dirname(__file__), "..", "..", "data")

location_definitions = parse_all_directory(data_dir)
