#!/usr/bin/env bash

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
