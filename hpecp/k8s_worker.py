from __future__ import absolute_import
from .logger import Logger

from operator import attrgetter
from tabulate import tabulate
import polling
from enum import Enum

try:
  basestring
except NameError:
  basestring = str

class WorkerK8sStatus(Enum):
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

    @staticmethod
    def status_names(indices=[]):
       return [ WorkerK8sStatus.status_name(i) for i in indices ]

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

class K8sWorkerController:

    def __init__(self, client):
        self.client = client


    def create_with_ssh_password(self, username, password):
        """Not Implemented yet"""
        raise NotImplementedError()

    def create_with_ssh_key(self, ip, ssh_key_data, tags=[]):
        '''Create a gateway instance using SSH key credentials to access the host

        Args:
            ip: str
                The IP address of the proxy host.  Used for internal communication.
            ssh_key_data: str
                The ssh key data as a string. 
            tags: list
                Tags to use, e.g. "{ 'tag1': 'foo', 'tag2', 'bar' }".

        Returns: Worker ID
        '''

        assert isinstance(ip, basestring), "'ip' must be provided and must be a string"
        assert isinstance(ssh_key_data, basestring), "'ssh_key_data' must be provided and must be a string"

        data = {
                "ipaddr": ip,
                "credentials": {
                    "type": "ssh_key_access",
                    "ssh_key_data": ssh_key_data
                },
                "tags": tags,
            }
             
        response = self.client._request(url='/api/v2/worker/k8shost/', http_method='post', data=data, description='worker/create_with_ssh_key')
        return response.headers['location']

    def list(self):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/api/v2/worker/k8shost/', http_method='get', description='worker/get_k8shosts')
        hosts = WorkerK8sList(response.json()['_embedded']['k8shosts'])
        return hosts

    def get(self, worker_id):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/api/v2/worker/k8shost/{}'.format(worker_id), http_method='get', description='worker/get_k8shosts')
        host = WorkerK8s(response.json())
        return host

    def delete(self, worker_id):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        self.client._request(url='/api/v2/worker/k8shost/{}'.format(worker_id), http_method='delete', description='worker/delete_k8shosts')

    # TODO rename status parameter to statuses
    def wait_for_status(self, worker_id, status=[], timeout_secs=60):
        """
        Uses: https://github.com/justiniso/polling/blob/master/polling.py

        status: WorkerK8sStatus value, e.g. WorkerK8sStatus.configured

        raises: Exception
        """
        assert len(status) > 0, "At least one 'status' must be provided"
        assert timeout_secs >= 0, "'timeout_secs' must be >= 0"

        # current_status = self.get_k8shost(worker_id).status

        # # if we aren't configuring,  we aren't going to change state
        # if current_status.find('configuring') < 0:
        #     raise Exception('Host status is: {} - not polling for an update'.format(current_status))

        try:
            polling.poll(
                lambda: self.get(worker_id).status in WorkerK8sStatus.status_names(status),
                step=10,
                poll_forever=False,
                timeout=timeout_secs
            )
        except polling.TimeoutException:
            status_names = [ WorkerK8sStatus.status_name(s) for s in status ]
            raise Exception(
                    "Timed out waiting for status(es): {} on K8S Worker: {}".format(
                        status_names, worker_id))



    def set_storage(self, worker_id, data):
        """
        Example:
        {"op_spec": {"persistent_disks": ["/dev/nvme2n1"], "ephemeral_disks": ["/dev/nvme1n1"]}, "op": "storage"}
        """
        self.client._request(url='/api/v2/worker/k8shost/{}'.format(worker_id), http_method='post', data=data, description='worker/add_k8shost')
        # no response - just status code

   