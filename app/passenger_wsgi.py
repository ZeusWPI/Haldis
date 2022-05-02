#!/usr/bin/env python3
"""
Used by Zeus in production.
This script makes Haldis acceptable to Phusion Passenger assuming a setup like on Zeus servers.
"""

# pylint: disable=wrong-import-position

import os
import sys

# User has the virtual environment in ~/env/
INTERP = os.path.expanduser("~/env/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

# Phusion Passenger expects this file to be called `passenger_wsgi.py`
# and the WSGI object to be called `application`
from app import create_app

# For running on the server with passenger etc
if __name__ == "__main__":
    application = create_app()
    application.run()
