#!/usr/bin/env bash

if [[ ! -d ~/.aws ]]; then
   echo "Please run 'aws configure'"
   exit 1
fi

if [[ ! -f ~/.aws_nacl_id ]]; then
    echo "Please input network acl id:"
    read NACL_ID
    echo "Saving network acl id to ~/.aws_nacl_id"
    echo $NACL_ID > ~/.aws_nacl_id
    echo "---"
fi
NACL_ID=$(cat ~/.aws_nacl_id)

if [[ ! -f ~/.aws_sg_id ]]; then
    echo "Please input security group id:"
    read SG_ID
    echo "Saving security group id to ~/.aws_sg_id"
    echo $SG_ID > ~/.aws_sg_id
    echo "---"
fi
SG_ID=$(cat ~/.aws_sg_id)

aws ec2 create-network-acl-entry \
    --network-acl-id $NACL_ID \
    --cidr-block "$(curl -s http://ifconfig.me/ip)/32" \
    --ingress \
    --protocol -1 \
    --rule-action allow \
    --rule-number 110

if [[ $? != 0 ]]; then
    aws ec2 replace-network-acl-entry \
        --network-acl-id $NACL_ID \
        --cidr-block "$(curl -s http://ifconfig.me/ip)/32" \
        --ingress \
        --protocol -1 \
        --rule-action allow \
        --rule-number 110
fi

aws ec2 default authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol all \
    --port -1 \
    --cidr "$(curl -s http://ifconfig.me/ip)/32"