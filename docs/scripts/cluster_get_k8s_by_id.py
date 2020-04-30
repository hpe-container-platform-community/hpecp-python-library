#!/usr/bin/env python3

from hpecp import ContainerPlatformClient, APIException
from hpecp.k8s_cluster import K8sClusterHostConfig

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
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session()

print( client.k8s_cluster.list().tabulate() )

first_cluster_id = 21 # client.k8s_cluster.list()[0].id

print( client.k8s_cluster.get(first_cluster_id) )
