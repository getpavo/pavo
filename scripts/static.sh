#!/bin/bash

if ! command -v poetry &> /dev/null
then
    echo "Poetry could not be found, cannot execute in virtual environment."
    exit
fi

poetry run python3 -m mypy ./pavo