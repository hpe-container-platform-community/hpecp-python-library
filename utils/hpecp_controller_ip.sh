#!/usr/bin/env bash

if [[ ! -d ~/.aws ]]; then
   echo "Please run 'aws configure'"
   exit 1
fi

if [[ ! -f ~/.aws_controller_id ]]; then
    echo "Please input controller instance id:"
    read CONTROLLER_ID
    echo "Saving controller instance id to ~/.aws_controller_id"
    echo $CONTROLLER_ID > ~/.aws_controller_id
    echo "---"
fi
CONTROLLER_ID=$(cat ~/.aws_controller_id)

echo -n "Controller public IP: "

aws ec2 describe-instances --instance-ids $CONTROLLER_ID --output text --query "Reservations[*].Instances[*].[PublicIpAddress]"

