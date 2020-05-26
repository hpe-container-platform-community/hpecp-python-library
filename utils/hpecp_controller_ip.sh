#!/usr/bin/env bash

set -u
set -e

if [[ ! -d ~/.aws || ! -f ~/.hpecp_service ]]; then
   echo "Please run utils/hpecp_configure.sh"
   exit 1
fi
source ~/.hpecp_service

aws ec2 describe-instances --instance-ids $CONTROLLER_INSTANCE_ID --output text --query "Reservations[*].Instances[*].[PublicIpAddress]"

