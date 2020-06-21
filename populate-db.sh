#!/bin/bash
set -euo pipefail

cd app
cp database/* .
python create_database.py setup_database
rm -f add_* create_database.py muhscheme
