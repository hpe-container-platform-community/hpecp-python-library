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

aws ec2 start-instances --instance-ids  $INSTANCE_IDS