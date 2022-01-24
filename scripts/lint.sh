#!/bin/bash

if ! command -v poetry &> /dev/null
then
    echo "Poetry could not be found, cannot execute in virtual environment."
    exit 1
fi

poetry run python3 -m pylint ./pavo