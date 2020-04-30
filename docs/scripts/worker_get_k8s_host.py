#!/usr/bin/env python3

from hpecp import ContainerPlatformClient
from hpecp.worker import WorkerK8sStatus
import argparse
import os
import urllib3

parser = argparse.ArgumentParser(description='Get K8S Worker Host.')
parser.add_argument('worker_id', metavar='worker_id', type=int, nargs=1, help='worker id (int)')
args = parser.parse_args()
worker_id = args.worker_id[0]

os.environ["LOG_LEVEL"] = "INFO"
# Disable the SSL warnings - don't do this on productions!  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl=False)

client.create_session()

host = client.worker.get_k8shost(worker_id=worker_id)
print("Found worker: " + str(host))

try:
    statuses=[ WorkerK8sStatus.configured ]
    client.worker.wait_for_k8shost_status(worker_id=worker_id, timeout_secs=10, status=statuses)
    print("Worker {} has status in {}".format(worker_id, WorkerK8sStatus.status_names(statuses)))
except:
    print("Time out waiting for host {} to have status of {}".format(worker_id, WorkerK8sStatus.status_names(statuses)))

try:
    statuses=[ WorkerK8sStatus.unlicensed ]
    client.worker.wait_for_k8shost_status(worker_id=worker_id, timeout_secs=40, status=statuses)
    print("Worker {} has status in {}".format(worker_id, WorkerK8sStatus.status_names(statuses)))
except:
    print("Time out waiting for host {} to have status of {}".format(worker_id, WorkerK8sStatus.status_names(statuses)))

