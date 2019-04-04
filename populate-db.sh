#!/bin/bash

cd app
cp database/* .
../venv/bin/python create_database.py
rm -f add_* create_database.py muhscheme
