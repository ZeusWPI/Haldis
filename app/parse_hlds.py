#!/usr/bin/env python3

from hlds.parser import parse_files

USAGE = """{0} [filename]...
Parse HLDS files, print as JSON

Without arguments, parse the default definitions.
With filenames as arguments, parse those files as HLDS.

{} --help         Print this help text"""


def main(filenames):
    if filenames:
        location_definitions = parse_files(filenames)
    else:
        from hlds.definitions import location_definitions

    print("\n\n".join(map(str, location_definitions)))


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print(USAGE.format(sys.argv[0]), file=sys.stderr)
    else:
        main(args)
