#!/bin/bash
# A simple file to run all instructions from the README
## this should be run in the root of the repository
pip3 install -r requirements.txt
cd app
cp config.example.py config.py
cp -t . database/*
python3 create_database.py
rm -f add_* create_database.py
python3 haldis.py runserver
cd ..
