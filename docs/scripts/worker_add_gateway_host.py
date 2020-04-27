#!/usr/bin/env python3

from hpecp import ContainerPlatformClient

client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session()

gateway_host_ip = '10.1.0.19' # None  # Set to  your Host IP Address
gateway_host_dns = "ip-10-1-0-19.eu-west-2.compute.internal"

if gateway_host_ip is None:
    raise Exception("Aborting. You must set the variable 'gateway_host_ip'.")

with open('/certs/controller.prv_key', 'r') as f:
    prvkey = f.read()

response = client.worker.add_gateway(
            data ={
                "ipaddr":gateway_host_ip,
                "credentials":{
                    "type":"ssh_key_access",
                    "ssh_key_data":prvkey
                },
                "tags":[],
                "proxy_nodes_hostname":gateway_host_dns,
                "purpose":"proxy"
            }
    )

print(response)
