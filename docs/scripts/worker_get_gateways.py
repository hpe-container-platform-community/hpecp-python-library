#!/usr/bin/env python3

from hpecp import ContainerPlatformClient
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

host = client.worker.get_gateways()[0]
print("Gateway: {} | {} | {} | {}".format( 
        host['_links']['self']['href'], 
        host['ip'], 
        host['purpose'], 
        host['state'] ))