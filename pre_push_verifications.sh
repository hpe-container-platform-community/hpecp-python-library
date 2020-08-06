#!/bin/bash

set -e

if [[  -d /home/theia/ ]]; 
then
    # black and isort have been installed in the 3.8.x pyenv
    eval "$(pyenv init -)"
    pyenv shell $(pyenv versions --bare | grep 3.8)
fi

isort tests/*.py hpecp/**.py bin/*.py
black bin/ tests/ hpecp/

#flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 --docstring-convention numpy bin/ hpecp/
flake8 --ignore=D,E501 tests/ # verify tests, but not for documentation

if [[  -d /home/theia/ ]]; 
then
    # ensure pyenvs are available to tox
    pyenv shell $(pyenv versions --bare)
fi

tox -- tests/

# coverage causes some tests to fail on PY3 so test it (issues 93)
#coverage3 erase && coverage3 run --source hpecp,bin setup.py test && coverage3 report -m