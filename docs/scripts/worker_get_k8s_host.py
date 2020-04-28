#!/usr/bin/env python3

from hpecp import ContainerPlatformClient
from hpecp.worker import WorkerK8sStatus

import os
os.environ["LOG_LEVEL"] = "INFO"

# Disable the SSL warnings - don't do this on productions!  
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl=False)

client.create_session()

host = client.worker.get_k8shost(worker_id=2)
print("Found host: " + str(host))

client.worker.wait_for_k8shost_status(worker_id=2, timeout_secs=5, status=WorkerK8sStatus.configured)
print("Host: 2 has status 'configured'")

client.worker.wait_for_k8shost_status(worker_id=2, timeout_secs=5, status=WorkerK8sStatus.deleting)
print("Host: 2 has status 'deleting'")