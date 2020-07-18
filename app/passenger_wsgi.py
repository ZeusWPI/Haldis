#!/usr/bin/env python3
"Script to run Haldis on a server"

import os
import sys

INTERP = os.path.expanduser("~/env/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())
from app import app as application

# For running on the server with passenger etc
if __name__ == "__main__":
    application.run()
