#!/bin/bash

# Makes a zip file to upload to lambda

rm nyc_school_food.zip

# shamelessly copied/pasted from https://stackoverflow.com/questions/28991015/python3-project-remove-pycache-folders-and-pyc-files
find . -type d -name __pycache__ \
     -o \( -type f -name '*.py[co]' \) -print0 \
    | xargs -0 sudo rm -rf

zip -r nyc_school_food.zip menu.py *.py
