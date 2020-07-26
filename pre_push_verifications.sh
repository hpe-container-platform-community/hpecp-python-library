#!/bin/bash

set -e

black bin/ tests/ hpecp/

#flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 --exclude hpecp/role.py --docstring-convention numpy bin/ hpecp/

tox -- tests/

# coverage causes some tests to fail on PY3 so test it (issues 93)
coverage3 erase && coverage3 run --source hpecp,bin setup.py test && coverage3 report -m