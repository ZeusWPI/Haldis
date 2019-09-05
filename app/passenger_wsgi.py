#!/usr/bin/env python

import os
import sys

from app import create_app

INTERP = os.path.expanduser("~/env/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

application = create_app()

# For running on the server with passenger etc
if __name__ == "__main__":
    application.run(port=8000)
