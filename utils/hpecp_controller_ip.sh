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

echo -n "Controller public IP: "

aws ec2 describe-instances --instance-ids $CONTROLLER_ID --output text --query "Reservations[*].Instances[*].[PublicIpAddress]"

