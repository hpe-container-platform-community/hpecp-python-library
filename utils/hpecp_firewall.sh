#!/usr/bin/env bash

set -u

if [[ ! -d ~/.aws  ]]; then
   if [[ ! -d /workspace/.aws ]]; then
       echo "Please run utils/hpecp_configure.sh"
       exit 1
   else
       ln -sf /workspace/.aws ~/.aws
   fi
fi

if [[ ! -f ~/.hpecp_service  ]]; then
   if [[ ! -f /workspace/.hpecp_service ]]; then
       echo "Please run utils/hpecp_configure.sh"
       exit 1
   else
       ln -sf /workspace/.hpecp_service ~/.hpecp_service
   fi
fi
source ~/.hpecp_service

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

aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol all \
    --port -1 \
    --cidr "$(curl -s http://ifconfig.me/ip)/32"
