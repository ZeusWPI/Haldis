#!/bin/bash
# A simple file to run all instructions from the README
## this should be run in the root of the repository

if [ ! -d "vent" ]; then
    python -m venv venv
fi

venv/bin/pip install -r requirements.txt
cd app
cp config.example.py config.py
cp -t . database/*
venv/bin/python create_database.py
rm -f add_* create_database.py
venv/bin/python haldis.py runserver
cd ..
