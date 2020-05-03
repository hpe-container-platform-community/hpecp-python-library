#!/usr/bin/env python3

from hpecp import ContainerPlatformClient, APIException
from hpecp.k8s_cluster import K8sClusterHostConfig
from kubernetes import client, config
import tempfile
import time
import os, sys
import urllib3

os.environ["LOG_LEVEL"] = "INFO"
# Disable the SSL warnings - don't do this on productions!  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

hpeclient = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

hpeclient.create_session()

print("\nHPE Container Platform K8S Clusters:\n")
for c in hpeclient.k8s_cluster.list():
    print("{:>12} {:>12} {:>12}".format(c.id, c.name, c.k))

cluster_list = hpeclient.k8s_cluster.list()
if len(cluster_list) == 0:
    print("No clusters found. Aborting.")
    sys.exit(1)
else:
    # get the kube admin config for the first cluster 
    admin_kube_config = cluster_list[0].admin_kube_config

    #  write it to a temporary file
    with tempfile.NamedTemporaryFile(mode = "w") as fp:
        fp.write(admin_kube_config)
        fp.flush()

        # read the kube config with the kubernetes client
        config.load_kube_config(fp.name)

        # list the pods        
        v1 = client.CoreV1Api()
        print("\nListing pods with their IPs:\n")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("{:>12}   {:>20}   {}".format(i.status.pod_ip, i.metadata.namespace, i.metadata.name))
