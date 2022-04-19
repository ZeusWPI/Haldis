#!/usr/bin/env bash
set -euo pipefail
# A simple file to run all instructions from the README
## this should be run in the root of the repository

bold=$(tput bold)
normal=$(tput sgr0)

B="\n${bold}"
E="${normal}"

if [ ! -d "venv" ]; then
	PYTHON_VERSION=$(cat .python-version)
	echo -e "${B} No venv found, creating a new one with version ${PYTHON_VERSION} ${E}"
	python3 -m virtualenv -p $PYTHON_VERSION venv
fi
source venv/bin/activate


echo -e "${B} Installing pip-tools ${E}"
pip install pip-tools

echo -e "${B} Downloading dependencies ${E}"
pip-sync

if [ ! -f app/config.py ]; then
	echo -e "${B} Copying config template. All custom config options can be set in the config.py file ${E}"
	cp app/config.example.py app/config.py
else
	echo -e "${B} Found existing config.py, not copying config teplate ${E}"
fi

echo -e "${B} Seeding database ${E}"
./populate-db.sh

if [ ! -d "menus" ]; then
	echo -en "${B} Do you want to use the Zeus HLDS menus? If not, you will have to clone your own menu repository. (Y/n) ${E}"
	read confirm
	if [ "$confirm" = n ]; then
		echo "Not cloning the Zeus HLDS menus"
	else
		git clone https://git.zeus.gent/haldis/menus.git
	fi
fi

echo -e "${B} Activate your venv using 'source venv/bin/activate'.\nThen run the development server with 'python app/app.py runserver' ${E}"
