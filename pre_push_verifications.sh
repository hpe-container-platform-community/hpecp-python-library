#!/bin/bash

set -e

black bin/ tests/ hpecp/
flake8 hpecp bin
tox -- tests/

# coverage causes some tests to fail on PY3 so test it (issues 93)
coverage3 erase && coverage3 run --source hpecp,bin setup.py test && coverage3 report -m