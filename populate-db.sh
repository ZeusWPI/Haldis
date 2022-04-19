#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/app"
cp database/* .
../venv/bin/python create_database.py setup_database
rm -f add_* create_database.py muhscheme.txt
