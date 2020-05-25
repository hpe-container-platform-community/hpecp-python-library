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

aws ec2 create-network-acl-entry \
    --network-acl-id $NACL_ID \
    --cidr-block "$(curl -s http://ifconfig.me/ip)/32" \
    --ingress \
    --protocol -1 \
    --rule-action allow \
    --rule-number 110 > /dev/null 2>&1

if [[ $? != 0 ]]; then
    aws ec2 replace-network-acl-entry \
        --network-acl-id $NACL_ID \
        --cidr-block "$(curl -s http://ifconfig.me/ip)/32" \
        --ingress \
        --protocol -1 \
        --rule-action allow \
        --rule-number 110 > /dev/null 2>&1
fi

aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol all \
    --port -1 \
    --cidr "$(curl -s http://ifconfig.me/ip)/32" > /dev/null 2>&1