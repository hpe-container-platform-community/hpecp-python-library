#!/bin/bash

set -e

pip3 install flake8 flake8-docstrings
flake8 --docstring-convention numpy bin/ hpecp/
flake8 --ignore=D tests/

black --check bin/ tests/ hpecp/

tox -- tests/