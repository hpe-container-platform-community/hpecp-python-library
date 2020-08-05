#!/bin/bash

set -e

isort tests/*.py
isort hpecp/**.py
isort bin/*.py

black bin/ tests/ hpecp/

#flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 --docstring-convention numpy bin/ hpecp/

flake8 --ignore=D,E501 tests/cli_test.py # don't verify documentation in tests

if [[] -d /home/theia/ ]]; 
then
    # ensure pyenvs are avaialble
    /home/theia/.pyenv/bin/pyenv local $(/home/theia/.pyenv/bin/pyenv versions --bare)
fi
tox --recreate -- tests/

echo "********** FIXME: tox should test py27 as well **********"

# coverage causes some tests to fail on PY3 so test it (issues 93)
#coverage3 erase && coverage3 run --source hpecp,bin setup.py test && coverage3 report -m


