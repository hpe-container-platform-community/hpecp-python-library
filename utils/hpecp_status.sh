#!/usr/bin/env bash

if [[ ! -d ~/.aws ]]; then
   echo "Please run 'aws configure'"
   exit 1
fi

if [[ ! -f ~/.hpecp_service ]]; then
    echo "Please create your ~/.hpecp_service file"
    exit 1
fi
source ~/.hpecp_service

aws ec2 describe-instance-status --instance-ids  $INSTANCE_IDS --include-all-instances --output table --query "InstanceStatuses[*].{ID:InstanceId,State:InstanceState.Name}"