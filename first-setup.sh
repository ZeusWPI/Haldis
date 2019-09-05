#!/bin/bash
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

echo -e "${B} Copying config template. All custom config options can be set in the config.py file ${E}"
cd app
cp config.example.py config.py
cd ..

echo -e "${B} Seeding database ${E}"
./populate-db.sh

echo -e "${B} Activate your venv using 'source venv/bin/activate'.\nThen run the server with 'python app/app.py runserver' ${E}"