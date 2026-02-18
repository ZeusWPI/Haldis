#!/usr/bin/env bash
set -euo pipefail

uv run python create_database.py setup_database
cd "$(dirname "$0")/app"
latest_revision=$(uv run flask db heads | sed "s/ (head)$//")
echo Stamping db at $latest_revision
uv run flask db stamp $latest_revision
