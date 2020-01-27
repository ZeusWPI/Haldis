#!/bin/bash
set -euo pipefail

# args = map(lambda arg: arg if x[0] in "/-" else pwd+arg, sys.argv[1:])
args=()
for i in "$@"; do
	# If argument is not an option and not an absolute path, it's a relative path: prepend current
	# working directory
	case "$i" in
		/*|-*) args[${#args[@]}]="$i"; ;;
		*)     args[${#args[@]}]="$PWD/$i"; ;;
	esac
done

cd "$(dirname "$0")/app"
exec ../venv/bin/python parse_hlds.py "${args[@]}"
