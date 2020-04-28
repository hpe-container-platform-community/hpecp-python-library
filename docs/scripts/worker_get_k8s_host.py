#!/usr/bin/env python3

from hpecp import ContainerPlatformClient
import os
os.environ["LOG_LEVEL"] = "INFO"

client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session()

host = client.worker.get_k8shost(worker_id=2)
print("Found host: " + str(host))

client.worker.wait_for_k8shost_status(worker_id=2, timeout_secs=5, status='configured')
print("Host: 2 has status 'configured'")

client.worker.wait_for_k8shost_status(worker_id=2, timeout_secs=5, status='blah')
