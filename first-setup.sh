#!/bin/bash
set -euo pipefail
# A simple file to run all instructions from the README
## this should be run in the root of the repository

bold=$(tput bold)
normal=$(tput sgr0)

B="\n${bold}"
E="${normal}"

if [ ! -d "venv" ]; then
	echo -e "${B} No venv found, creating a new one ${E}"
	python3 -m venv venv
fi
source venv/bin/activate


echo -e "${B} Installing pip-tools ${E}"
pip install pip-tools

echo -e "${B} Downloading dependencies ${E}"
pip-sync

echo -en "${B} Do you want to install support for the Airbrake API for error logging? If you don't have an Errbit server or Airbrake account, answer no. (y/N) ${E}"
read confirm
if [ "$confirm" = y ]; then
	pip install airbrake
else
	echo "Not installing airbrake"
fi

if [ ! -f app/config.py ]; then
	echo -e "${B} Copying config template. All custom config options can be set in the config.py file ${E}"
	cp app/config.example.py app/config.py
else
	echo -e "${B} Found existing config.py, not copying config teplate ${E}"
fi

echo -e "${B} Seeding database ${E}"
./populate-db.sh

echo -e "${B} Activate your venv using 'source venv/bin/activate'.\nThen run the development server with 'python app/app.py runserver' ${E}"
