#!/usr/bin/env bash

# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

set -u
set -e

# NOTE: we save settings to /workspace as the $HOME folder isn't persisted in gitpod

[[ -f ~/.hpecp_service ]] && echo Aborting '~/.hpecp_service' exists && exit 1
[[ -d ~/.aws ]] && echo 'Aborting ~/.aws exists' && exit 1

rm -f /workspace/.hpecp_service
rm -rf /workspace/.aws

if [[ ! -f ~/.hpecp_service ]]; then
    echo "Enter your HPECP service details (enter empty line to finish):"

	while read line
	do
		# break if the line is empty
		[ -z "$line" ] && break
		echo "$line" >> "/workspace/.hpecp_service"
	done
	ln -sf /workspace/.hpecp_service ~/.hpecp_service
fi
source ~/.hpecp_service

if [[ ! -f ~/.aws ]]; then
	mkdir /workspace/.aws
	cat <<-EOF > /workspace/.aws/credentials
		[default]
		aws_secret_access_key = ${AWS_SECRET_KEY}
		aws_access_key_id = ${AWS_ACCESS_KEY}
	EOF
	cat <<-EOF > /workspace/.aws/config
		[default]
		region = ${AWS_REGION}
	EOF
	ln -sf /workspace/.aws ~/.aws
fi
