#!/usr/bin/env bash

set -u
set -e

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

aws ec2 start-instances --instance-ids $ALL_INSTANCE_IDS