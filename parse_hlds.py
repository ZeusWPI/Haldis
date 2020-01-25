#!/usr/bin/env python3

import json
from tatsu.util import asjson
from app.hlds.loader import parse_files


USAGE = """{0} [filename]...
Parse HLDS files, print as JSON

Without arguments, parse the default definitions.
With filenames as arguments, parse those files as HLDS.

{} --help         Print this help text"""


def definitions():
    from app.hlds.definitions import location_definitions
    return location_definitions


def main(filenames):
    locations = parse_files(filenames) if filenames else definitions()
    print(json.dumps(asjson(locations), indent="\t"))


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print(USAGE.format(sys.argv[0]), file=sys.stderr)
    else:
        main(args)
