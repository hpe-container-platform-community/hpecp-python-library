#!/bin/bash

set -e

black bin/ tests/ hpecp/
flake8 hpecp bin
tox -- tests/