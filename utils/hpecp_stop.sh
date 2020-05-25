#!/usr/bin/env bash

if [[ ! -d ~/.aws ]]; then
   echo "Please run 'aws configure'"
   exit 1
fi

if [[ ! -f ~/.aws_instance_ids ]]; then
    echo "Please input a list of instance ids, separated by whitespace:"
    read INSTANCE_IDS
    echo "Saving instance ids to ~/.aws_instance_ids"
    echo $INSTANCE_IDS > ~/.aws_instance_ids
fi

INSTANCE_IDS=$(cat ~/.aws_instance_ids)

aws ec2 stop-instances --instance-ids  $INSTANCE_IDS