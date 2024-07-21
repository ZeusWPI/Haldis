# Import this class to load the standard HLDS definitions
import subprocess
from pathlib import Path
from typing import List

from .location_extender import extend_locations

from .models import Location
from .parser import parse_all_directory

__all__ = ["location_definitions", "location_definition_version"]

# pylint: disable=invalid-name

# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "menus"

location_definitions: List[Location] = parse_all_directory(str(DATA_DIR))

def extend_locations_with_osm(app) -> None:
    global location_definitions
    location_definitions = extend_locations(app, location_definitions)
    location_definitions.sort(key=lambda l: l.name, reverse=True)

try:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, cwd=str(ROOT_DIR), check=True)
    location_definition_version = proc.stdout.decode().strip()
except FileNotFoundError:
    location_definition_version = ""
