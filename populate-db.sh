#!/usr/bin/env bash
set -euo pipefail

env python create_database.py setup_database
cd "$(dirname "$0")/app"
latest_revision=$(env flask db heads | sed "s/ (head)$//")
echo Stamping db at $latest_revision
env flask db stamp $latest_revision
