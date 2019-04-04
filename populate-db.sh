#!/bin/bash

cd app
cp database/* .
python create_database.py
rm -f add_* create_database.py muhscheme
