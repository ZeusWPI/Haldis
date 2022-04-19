#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/app"

env python create_database.py setup_database
