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

class WorkerK8sStatus():
    
    bundle = 1
    installing = 2
    installed = 3
    ready = 4
    unlicensed = 5
    configuring = 6
    configured = 7
    error = 8
    sysinfo = 9 
    unconfiguring = 10 
    deleting = 11
    storage_pending = 12 
    storage_configuring = 13
    storage_error = 14

    @staticmethod
    def status_name(index):
        items = {v: k for k, v in WorkerK8sStatus.__dict__.items()}
        return items[index]

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
        response = self.client._request(url='/api/v2/worker/k8shost/', http_method='get', description='worker/get_k8shosts')
        hosts = WorkerK8sList(response.json()['_embedded']['k8shosts'])
        return hosts

    def get_k8shost(self, worker_id):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/api/v2/worker/k8shost/{}'.format(worker_id), http_method='get', description='worker/get_k8shosts')
        host = WorkerK8s(response.json())
        return host

    def wait_for_k8shost_status(self, worker_id, status=None, timeout_secs=60):
        """
        Uses: https://github.com/justiniso/polling/blob/master/polling.py

        status: WorkerK8sStatus value, e.g. WorkerK8sStatus.configured

        raises: Exception
        """
        assert status is not None, "'status' must be provided"
        #TODO assert status is WorkerK8sStatus value
        assert timeout_secs >= 0, "'timeout_secs' must be >= 0"

        # current_status = self.get_k8shost(worker_id).status

        # # if we aren't configuring,  we aren't going to change state
        # if current_status.find('configuring') < 0:
        #     raise Exception('Host status is: {} - not polling for an update'.format(current_status))

        try:
            polling.poll(
                lambda: self.get_k8shost(worker_id).status == status,
                step=10,
                poll_forever=False,
                timeout=timeout_secs
            )
        except polling.TimeoutException:
            raise Exception(
                    "Timed out waiting for status: '{}' on K8S Worker: {}".format(
                        WorkerK8sStatus.status_name(status), worker_id))

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
        response = self.client._request(url='/api/v2/worker/k8shost/', http_method='post', data=data, description='worker/add_k8shost')
        return response

    def add_gateway(self, data):
        '''
        Example:
            data = {
                "ip":"10.1.0.105",
                "credentials":{
                    "type":"ssh_key_access",
                    "ssh_key_data":"-----BEGIN RSA PRIVATE KEY-----...-----END RSA PRIVATE KEY-----\n"
                },
                "tags":[],
                "proxy_nodes_hostname":"ip-10-1-0-19.eu-west-2.compute.internal",
                "purpose":"proxy"
            },
        '''
        response = self.client._request(url='/api/v1/workers/', http_method='post', data=data, description='worker/add_gateway')
        return response

    def get_gateways(self):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/api/v1/workers/', http_method='get', description='worker/get_gateways')
        return [ worker for worker in response.json()["_embedded"]["workers"] if worker['purpose'] == 'proxy' ]

    def get_gateway(self, id):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/api/v1/workers/', http_method='get', description='worker/get_gateways')
        workers = response.json()["_embedded"]["workers"]
        return [ worker for worker in workers if worker['purpose'] == 'proxy' and worker['_links']['self']['href'].split('/')[-1] == str(id) ][0]

    def wait_for_gateway_state(self, id, state=[], timeout_secs=60):
        """
        Uses: https://github.com/justiniso/polling/blob/master/polling.py

        status: WorkerK8sStatus value, e.g. WorkerK8sStatus.configured

        raises: Exception
        """
        assert timeout_secs >= 0, "'timeout_secs' must be >= 0"

        try:
            polling.poll(
                lambda: self.get_gateway(id)['state'] in state,
                step=10,
                poll_forever=False,
                timeout=timeout_secs
            )
        except polling.TimeoutException:
            message = "Timed out waiting for status: '{}' on Gateway ID: {}".format(state, id)
            self.client.log.error(message)
            raise Exception(message)

        self.client.log.info("Gateway ID: {} was detected to have state {}".format(id, state))