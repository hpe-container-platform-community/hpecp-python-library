#!/usr/bin/env python3

from hpecp import ContainerPlatformClient

client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session()

hosts = client.worker.get_k8shosts()

for h in hosts:
    print("{} | {} | {} | {} | {}".format(h.worker_id, h.hostname, h.ipaddr, h.status, h.href))
