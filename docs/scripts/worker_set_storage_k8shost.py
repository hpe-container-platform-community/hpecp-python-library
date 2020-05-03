#!/usr/bin/env python3

from hpecp import ContainerPlatformClient
from hpecp.worker import WorkerK8sStatus
import os
import argparse

os.environ["LOG_LEVEL"] = "INFO"

parser = argparse.ArgumentParser(description='Get K8S Worker Host.')
parser.add_argument('worker_id', metavar='worker_id', type=int, nargs=1,
                   help='worker id (int)')

args = parser.parse_args()
worker_id = args.worker_id[0]


client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session()

# wait 20 minutes
client.worker.wait_for_k8shost_status(worker_id=worker_id, timeout_secs=1200, status=[ WorkerK8sStatus.storage_pending ])

data = {"op_spec": {"persistent_disks": ["/dev/nvme2n1"], "ephemeral_disks": ["/dev/nvme1n1"]}, "op": "storage"}
client.worker.set_storage_k8shost(worker_id=worker_id, data=data)

# wait 20 minutes
client.worker.wait_for_k8shost_status(worker_id=worker_id, timeout_secs=1200, status=[ WorkerK8sStatus.ready ])
