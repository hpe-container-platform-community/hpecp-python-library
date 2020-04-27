#!/usr/bin/env python3

from hpecp import ContainerPlatformClient

client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session()

################
# Add K8S host # 
################

k8s_host_ip = None  # Set to  your Host IP Address

if k8s_host_ip is None:
    raise Exception("Aborting. You must set the variable 'k8s_host_ip'.")

with open('/certs/controller.prv_key', 'r') as f:
    prvkey = f.read()

client.worker.add_k8shost(
            data ={
                "ipaddr":k8s_host_ip,
                "credentials":{
                    "type":"ssh_key_access",
                    "ssh_key_data":prvkey
                },
                "tags":[]
            }
    )
