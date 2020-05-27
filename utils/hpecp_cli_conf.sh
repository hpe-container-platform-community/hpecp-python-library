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

CONTROLLER_IP=$(aws ec2 describe-instances --instance-ids $CONTROLLER_INSTANCE_ID --output text --query "Reservations[*].Instances[*].[PublicIpAddress]")

if [[ "${INSTALL_WITH_SSL}" == 'true' ]]; then
   SSL=True
else
   SSL=False
fi

echo "[default]
api_host = ${CONTROLLER_IP}
api_port = 8080
use_ssl = ${SSL}
verify_ssl = False
warn_ssl = False
username = admin
password = admin123
"

