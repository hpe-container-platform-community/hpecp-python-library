from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
from operator import attrgetter
import time
import requests
import json
from tabulate import tabulate

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

class WorkerK8s():

    @staticmethod
    def __class_dir__():
        return [ 'worker_id', 'status', 'hostname', 'ipaddr', 'href' ]

    def __init__(self, json):
        self.json = json
    
    def __dir__(self):
        return WorkerK8s.__class_dir__()

    def __getitem__(self, item):
        return getattr(self, self.__dir__()[item])

    @property
    def worker_id(self): return int(self.json['_links']['self']['href'].split('/')[-1])

    @property
    def status(self): return self.json['status']

    @property
    def hostname(self): return self.json['hostname']

    @property
    def ipaddr(self): return self.json['ipaddr']

    @property
    def href(self): return self.json['_links']['self']['href']

    def __len__(self):
        return len(dir(self))

class WorkerK8sList():

    def __init__(self, json):
        self.json = json
        self.tenants = sorted([WorkerK8s(t) for t in json],  key=attrgetter('worker_id'))

    def __getitem__(self, item):
        return self.tenants[item]

    def next(self):
        if not self.tenants:
           raise StopIteration
        return self.tenants.pop(0)

    # TODO do we need  both next() and __next__()?
    def __next__(self):
        if not self.tenants:
           raise StopIteration
        return self.tenants.pop(0)

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.tenants)

    def tabulate(self):
        return tabulate(self, headers=WorkerK8s.__class_dir__(), tablefmt="pretty")

class WorkerController:

    def __init__(self, client):
        self.client = client

    def get_k8shosts(self):
        response = self.client._request(url='/v2/worker/k8shost/', http_method='get', description='worker/get_k8shosts')
        hosts = WorkerK8sList(response.json()['_embedded']['k8shosts'])
        return hosts

    def add_k8shost(self, data):
        '''
        Example:
        
            data = {
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

    def add_gateway(self, data):
        '''
        Example:
            data = {
                "ipaddr":"10.1.0.105",
                "credentials":{
                    "type":"ssh_key_access",
                    "ssh_key_data":"-----BEGIN RSA PRIVATE KEY-----...-----END RSA PRIVATE KEY-----\n"
                },
                "tags":[],
                "proxy_nodes_hostname":"ip-10-1-0-19.eu-west-2.compute.internal",
                "purpose":"proxy"
            },
        '''
        response = self.client._request(url='/v1/workers/', http_method='post', data=data, description='worker/add_gateway')
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