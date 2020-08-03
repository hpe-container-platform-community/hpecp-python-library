#!/bin/bash

set -e

isort --check-only tests/*.py bin/*.py hpecp/**.py

black bin/ tests/ hpecp/

#flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 --exclude hpecp/role.py --docstring-convention numpy bin/ hpecp/

flake8 --ignore=D,E501 tests/catalog_test.py tests/base_test.py tests/cli_test.py

tox -e py35 -- tests/

echo "********** FIXME: tox should test py27 as well **********"

# coverage causes some tests to fail on PY3 so test it (issues 93)
#coverage3 erase && coverage3 run --source hpecp,bin setup.py test && coverage3 report -m


