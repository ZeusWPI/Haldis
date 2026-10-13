#!/bin/sh
set -eu
cd "$(dirname "$0")"
. ./.venv/bin/activate
for menu in menus/*.hlds; do
    echo $menu:
    python -c "from app.hlds.parser import parse_file; parse_file('$menu')" | nl
done
