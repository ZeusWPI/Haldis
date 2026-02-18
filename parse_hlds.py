#!/usr/bin/env python3
"Module used for parsing the HLDS files"

import json
import sys

#from IPython import embed as ipy

from app.hlds.parser import parse_files


class JSONViaDictEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

if __name__ == "__main__":
    filenames = sys.argv[1:]
    if len(filenames) == 0:
        print(f"Usage: {sys.argv[0]} [filename]...", file=sys.stderr)
        print("Parse HLDS files, print as JSON", file=sys.stderr)
        print("Note: can (?) return multiple objects per file", file=sys.stderr)
    else:
        locations = parse_files(filenames)
        print(json.dumps(locations, cls=JSONViaDictEncoder, indent=4))
