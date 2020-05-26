#!/usr/bin/env bash

set -u
set -e

if [[ ! -d ~/.aws || ! -f ~/.hpecp_service ]]; then
   echo "Please run utils/hpecp_configure.sh"
   exit 1
fi
source ~/.hpecp_service

aws ec2 describe-instance-status --instance-ids  $ALL_INSTANCE_IDS --include-all-instances --output table --query "InstanceStatuses[*].{ID:InstanceId,State:InstanceState.Name}"