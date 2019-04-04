#!/bin/bash
# A simple file to run all instructions from the README
## this should be run in the root of the repository

if [ ! -d "venv" ]; then
    echo "No venv found, creating a new one"
    python -m venv venv
fi

source venv/bin/activate

echo "Downloading dependencies"
pip-sync

echo "Copying config template. All custom config options can be set in the config.py file"
cd app
cp config.example.py config.py
cd ..

echo "Seeding database"
./populate-db.sh

echo "You can now run the server with 'python app/haldis.py runserver'"
