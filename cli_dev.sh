#!/bin/bash

set -x
set -e

pip install -e .

hpecp autocomplete bash > ~/hpecp_completion.sh

source ~/hpecp_completion.sh
