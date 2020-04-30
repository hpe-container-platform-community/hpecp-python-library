#!/usr/bin/env python3

from hpecp import ContainerPlatformClient
from hpecp.k8s_cluster import K8sClusterHostConfig

client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session()

print( client.k8s_worker.get_k8shosts().tabulate() )

k8shosts_config=[ 
    K8sClusterHostConfig(4, 'worker'),
    K8sClusterHostConfig(5, 'master')
    ]

k8s_cluster_id = client.k8s_cluster.create(name='def', description='my cluster', k8s_version='1.17.0', k8shosts_config=k8shosts_config)
print('creating cluster id: ' + k8s_cluster_id)