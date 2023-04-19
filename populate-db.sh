#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/app"

env python create_database.py setup_database
latest_revision=$(env python app.py db heads | sed "s/ (head)$//")
echo Stamping db at $latest_revision
env python app.py db stamp $latest_revision
