from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
import time
import requests
import json

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

class WorkerController:

    def __init__(self, client):
        self.client = client

    def add_k8shost(self, data):
        '''
        Example:
        
            data ={
                "ipaddr":"10.1.0.105",
                "credentials":{
                    "type":"ssh_key_access",
                    "ssh_key_data":"-----BEGIN RSA PRIVATE KEY-----...-----END RSA PRIVATE KEY-----\n"
                },
                "tags":[]
            },
        '''
        response = self.client._request(url='/v2/worker/k8shost/', http_method='post', data=data, description='worker/add_k8shost')
        return response


# get k8s workers()
#
# request: {"method":"get","apiurl":"https://127.0.0.1:8080/api/v2/worker/k8shost/","timeout":29,"data":null,"op":""}
# response: {"_embedded": {"k8shosts": [
#   {
#       "status": "unlicensed", 
#       "propinfo": {
#           "bds_storage_apollo": "false", 
#           "bds_network_publicinterface": "ens5"
#       }, 
#       "approved_worker_pubkey": [], 
#       "tags": [], 
#       "hostname": "ip-10-1-0-238.eu-west-2.compute.internal", 
#       "ipaddr": "10.1.0.238", 
#       "setup_log": "/var/log/bluedata/install/k8shost_setup_10.1.0.238-2020-4-26-18-41-16", 
#       "_links": {
#           "self": {"href": "/api/v2/worker/k8shost/4"}
#       }, 
#       "sysinfo": {
#           "network": [ ... ],
#           "keys": { "reported_worker_public_key": "ssh-rsa ...== server\n" }, 
#           "storage": [ ... ], 
#           "swap": {"swap_total": 0}, 
#           "memory": {"mem_total": 65842503680}, 
#           "gpu": {"gpu_count": 0}, 
#           "cpu": {"cpu_logical_cores": 16, "cpu_count": 8, "cpu_physical_cores": 8, "cpu_sockets": 1}, 
#           "mountpoint": []
#       }
# }, 
# {
#       "status": "bundle", 
#       "approved_worker_pubkey": [], 
#       "tags": [], 
#       "hostname": "", 
#       "ipaddr": "10.1.0.186", 
#       "setup_log": "/var/log/bluedata/install/k8shost_setup_10.1.0.186-2020-4-26-18-49-10", 
#       "_links": {"self": {"href": "/api/v2/worker/k8shost/5"}}
# }, 
# {
#       "status": "bundle", 
#       "approved_worker_pubkey": [], 
#       "tags": [], 
#       "hostname": "", 
#       "ipaddr": "10.1.0.227", 
#       "setup_log": "/var/log/bluedata/install/k8shost_setup_10.1.0.227-2020-4-26-18-49-23", 
#       "_links": {"self": {"href": "/api/v2/worker/k8shost/6"}}
# }
# ]}, "_links": {"self": {"href": "/api/v2/worker/k8shost"}}}