# Import this class to load the standard HLDS definitions

import subprocess
from os import path
from typing import List

from .models import Location
from .parser import parse_all_directory

__all__ = ["location_definitions", "location_definition_version"]

# pylint: disable=invalid-name

# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
DATA_DIR = path.join(path.dirname(__file__), "..", "..", "menus")

location_definitions: List[Location] = parse_all_directory(DATA_DIR)
location_definitions.sort(key=lambda l: l.name)

proc = subprocess.run(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, check=True)
location_definition_version = proc.stdout.decode().strip()
