#!/usr/bin/env python3

from hpecp import ContainerPlatformClient
import os
os.environ["LOG_LEVEL"] = "DEBUG"

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

gateway_host_ip = '10.1.0.233' # None  # Set to  your Host IP Address
gateway_host_dns = "ip-10-1-0-233.eu-west-2.compute.internal"

if gateway_host_ip is None:
    raise Exception("Aborting. You must set the variable 'gateway_host_ip'.")

with open('/certs/controller.prv_key', 'r') as f:
    prvkey = f.read()

response = client.worker.add_gateway(
            data ={
                "ip":gateway_host_ip,
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
