from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
from operator import attrgetter
import time
import requests
import json
from tabulate import tabulate
import polling

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

class WorkerK8s():

    @staticmethod
    def __class_dir__():
        return [ 'worker_id', 'status', 'hostname', 'ipaddr', 'href' ]

    def __repr__(self):
        return "<WorkerK8S worker_id:{} status:{} ipaddr:{}>".format( self.worker_id, self.status, self.ipaddr)

    def __str__(self):
        return "WorkerK8s(worker_id={}, status={}, ipaddr={})".format(
                    self.worker_id, self.status, self.ipaddr)

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
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/v2/worker/k8shost/', http_method='get', description='worker/get_k8shosts')
        hosts = WorkerK8sList(response.json()['_embedded']['k8shosts'])
        return hosts

    def get_k8shost(self, worker_id):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/v2/worker/k8shost/{}'.format(worker_id), http_method='get', description='worker/get_k8shosts')
        host = WorkerK8s(response.json())
        return host

    def wait_for_k8shost_status(self, worker_id, status=None, timeout_secs=60):
        assert status is not None, "'status' must be provided"
        assert timeout_secs >= 0, "'timeout_secs' must be >= 0"
        try:
            polling.poll(
                lambda: self.get_k8shost(worker_id).status == status,
                step=60,
                poll_forever=False,
                timeout=timeout_secs
            )
        except polling.TimeoutException:
            raise TimeoutError("Timed out waiting for status: '{}' on K8S Worker: {}".format(status, worker_id))

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
