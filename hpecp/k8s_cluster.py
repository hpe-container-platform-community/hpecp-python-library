from __future__ import absolute_import
from .logger import Logger

import json
from operator import attrgetter
from tabulate import tabulate
import polling
from enum import Enum
import re

import sys
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring

class K8sClusterStatus(Enum):
    ready = 1
    creating = 2
    updating = 3
    upgrading = 4
    deleting = 5
    error = 6
    warning = 7


class K8sCluster():
    """
    """

    all_fields = [ 'id', 'name', 'description', 'k8s_version', 'created_by_user_id', 'created_by_user_name', 'created_time', 'status' ]

    @staticmethod
    def __class_dir__():
        return K8sCluster.all_fields

    def __repr__(self):
        return "<K8sCluster id:{} name:{} description:{} status:{}>".format( self.id, self.name, self.description, self.status)

    def __str__(self):
        return "K8sCluster(id={}, name={}, description={}, status={})".format(
                    self.id, self.name, self.description, self.status)

    def __init__(self, json):
        self.json = json
        self.columns = K8sCluster.__class_dir__()
    
    def __dir__(self):
        return self.columns
        #return K8sCluster.__class_dir__()

    def __getitem__(self, item):
        return getattr(self, self.__dir__()[item])

    def set_columns(self, columns):
        self.columns = columns

    @property
    def id(self): return self.json['_links']['self']['href']

    @property
    def name(self): return self.json['label']['name']

    @property
    def description(self): return self.json['label']['description']

    @property
    def k8s_version(self): return self.json['k8s_version']

    @property
    def created_by_user_id(self): return self.json['created_by_user_id']

    @property
    def created_by_user_name(self): return self.json['created_by_user_name']

    @property
    def created_time(self): return self.json['created_time']

    @property
    def k8shosts_config(self): return self.json['k8shosts_config']

    @property
    def admin_kube_config(self): return self.json['admin_kube_config']

    @property
    def dashboard_token(self): return self.json['dashboard_token']

    @property
    def api_endpoint_access(self): return self.json['api_endpoint_access']

    @property
    def dashboard_endpoint_access(self): return self.json['dashboard_endpoint_access']

    @property
    def cert_data(self):
        try:
            return self.json['cert_data']
        except KeyError:
            return None

    @property
    def status(self): return self.json['status']

    @property
    def status_message(self): return self.json['status_message']

    @property
    def _links(self): return self.json['_links']

    def __len__(self):
        return len(dir(self))

class K8sClusterList():
    """[summary]
    """

    def __init__(self, json):
        """[summary]

        Arguments:
            json {[type]} -- [description]
        """
        self.json = json
        self.clusters = sorted([K8sCluster(t) for t in json],  key=attrgetter('id'))
        self.tenant_columns = K8sCluster.all_fields

    def __getitem__(self, item):
        return self.clusters[item]

    # Python 2
    def next(self):
        if not self.clusters:
           raise StopIteration
        tenant = self.clusters.pop(0)
        tenant.set_columns(self.tenant_columns)
        return tenant

    # Python 3
    def __next__(self):
        if not self.clusters:
           raise StopIteration
        tenant = self.clusters.pop(0)
        tenant.set_columns(self.tenant_columns)
        return tenant

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.clusters)

    def tabulate(self, columns=K8sCluster.all_fields):
        """Provide a tabular represenation of the Cluster List

        Keyword Arguments:
            columns {list[str]} -- list of columns to return in the table (default: {K8sCluster.all_fields})

        Returns:
            str -- table output

        Example:
            # Print the cluster list with all the fields
            print(hpeclient.cluster.list().tabulate())

            # Print the cluster list with a subset of the fields
            print(hpeclient.cluster.list().tabulate(columns=['id', 'name', 'description']))
        """
        if columns != K8sCluster.all_fields:
            assert isinstance(columns, list), "'columns' parameter must be list"
            for field in K8sCluster.all_fields:
                assert field in K8sCluster.all_fields, "item '{}' is not a field in K8sCluster.all_fields".format(field)

        self.tenant_columns = columns
        return tabulate(self, headers=columns, tablefmt="pretty")

class K8sClusterHostConfig():
    """[summary]
    """
    def __init__(self, node, role):
        """[summary]

        Arguments:
            node {[type]} -- [description]
            role {[type]} -- [description]
        """
        assert isinstance(node, string_types), "'node' must be an string"
        assert re.match(r'\/api\/v2\/worker\/k8shost\/[0-9]+', node), "'node' must have format '/api/v2/worker/k8shost/[0-9]+'"
        assert role in [ 'master', 'worker' ], "'role' must one of ['master, worker']"

        self.node = node
        self.role = role

    def to_dict(self):
        """[summary]

        Returns:
            [type] -- [description]
        """
        return { 
                'node': self.node, 
                'role': self.role 
            }
        
class K8sClusterController:
    """[summary]
    """

    def __init__(self, client):
        """[summary]

        Arguments:
            client {[type]} -- [description]
        """
        self.client = client

    def create(self, 
                name=None, 
                description=None, 
                k8s_version=None,
                pod_network_range='10.192.0.0/12', 
                service_network_range='10.96.0.0/12',
                pod_dns_domain='cluster.local',
                persistent_storage_local=False,
                persistent_storage_nimble_csi=False,
                k8shosts_config = [],
                ):
        """[summary]

        Keyword Arguments:
            name {[type]} -- [description] (default: {None})
            description {[type]} -- [description] (default: {None})
            k8s_version {[type]} -- [description] (default: {None})
            pod_network_range {str} -- [description] (default: {'10.192.0.0/12'})
            service_network_range {str} -- [description] (default: {'10.96.0.0/12'})
            pod_dns_domain {str} -- [description] (default: {'cluster.local'})
            persistent_storage_local {bool} -- [description] (default: {False})
            persistent_storage_nimble_csi {bool} -- [description] (default: {False})
            k8shosts_config {list} -- [description] (default: {[]})

        Returns:
            [type] -- [description]
        """

        # Create a K8S Cluster.
        #     name: required, at least 1 characters
        #     description: defaults to empty string if not provided
        #     k8s_version: Kubernetes version to configure. If not specified defaults to the latest version as supported by the rpms.
        #     pod_network_range: Network range to be used for kubernetes pods. Defaults to 10.192.0.0/12
        #     service_network_range: Network range to be used for kubernetes services that are exposed with Cluster IP. Defaults to 10.96.0.0/12
        #     pod_dns_domain: DNS Domain to be used for kubernetes pods. Defaults to cluster.local
        #     persistent_storage_local: Enables local host storage to be available in the kubernetes cluster
        #     persistent_storage_nimble_csi: Installs the Nimble CSI plugin for Nimble storage to be available in the kubernetes cluster
        #     k8shosts_config: list of K8sClusterHostConfig objects
        #     int: The ID for the K8S Cluster with format '/api/v2/k8scluster/[0-9]+'
        #     APIException

        assert isinstance(name, string_types) and len(name) > 0,"'name' must be provided and must be a string"
        assert description is None or isinstance(description, string_types), "'description' if provided, must be a string"
        assert k8s_version is None or isinstance(k8s_version, string_types), "'k8s_version' if provided, must be a string"
        assert isinstance(pod_network_range, string_types), "'pod_network_range' must be a string"
        assert isinstance(service_network_range, string_types), "'service_network_range' must be a string"
        assert isinstance(pod_dns_domain, string_types), "'pod_dns_domain' must be a string"
        assert isinstance(persistent_storage_local, bool), "'persistent_storage_local' must be True or False"
        assert isinstance(persistent_storage_nimble_csi, bool), "'persistent_storage_nimble_csi' must be True or False"
        assert isinstance(k8shosts_config, list), "'k8shosts_config' must be a list"
        assert len(k8shosts_config) > 0, "'k8shosts_config' must have at least one item"
        for i, conf in enumerate(k8shosts_config):
            assert isinstance(conf, K8sClusterHostConfig), "'k8shosts_config' item '{}' is not of type K8sClusterHostConfig".format(i)

        data = {
            'label': { 
                'name': name
            },
            'pod_network_range': pod_network_range,
            'service_network_range': service_network_range,
            'pod_dns_domain': pod_dns_domain,
            'persistent_storage': { 
                'local': persistent_storage_local,
                'nimble_csi': persistent_storage_nimble_csi
            },
            'k8shosts_config': [ c.to_dict() for c in k8shosts_config ]
        }
        if description is not None: data['label']['description'] = description
        if k8s_version is not None: data['k8s_version'] = k8s_version

        response = self.client._request(url='/api/v2/k8scluster', http_method='post', data=data, description='k8s_cluster/create')
        return response.headers['Location']

    def list(self):
        """Retrieve list of K8S Clusters.

        Returns:
            K8sClusterList: List of K8s Clusters
            
        Raises:
            APIException
        """
        response = self.client._request(url='/api/v2/k8scluster', http_method='get', description='k8s_cluster/list')
        return K8sClusterList(response.json()['_embedded']['k8sclusters'])

    def get(self, k8scluster_id, setup_log=False):
        """Retrieve a K8S Cluster details.

        Args:
            k8scluster_id: (int) the K8S cluster ID
            setup_log: (bool) set to True to return the cluster setup log

        Returns:
            K8sCluster: object representing K8S Cluster
            
        Raises:
            APIException
        """
        assert isinstance(k8scluster_id, str),"'k8scluster_id' must be provided and must be a string"
        assert re.match(r'\/api\/v2\/k8scluster\/[0-9]+', k8scluster_id), "'k8scluster_id' must have format '/api/v2/worker/k8scluster/[0-9]+'"

        if setup_log == True:
            params = '?setup_log'
        else:
            params = ''

        response = self.client._request(url='{}{}'.format(k8scluster_id, params), http_method='get', description='k8s_cluster/get')
        return K8sCluster(response.json())

    def wait_for_status(self, k8scluster_id, status=[], timeout_secs=60):
        """Wait for cluster status.

        Args:
            k8scluster_id: (int) the K8S cluster ID
            status: (list) of type K8sClusterStatus status(es) to wait for.  
                    Use an empty array if you want to wait for a cluster's existence to cease.
            timeout_secs: (int) how long to wait for the status(es)

        Returns:
            bool: True if status was found before timeout, otherwise False
            
        Raises:
            APIItemNotFoundException: if the item is not found
            APIException: if a generic API exception occurred
        """
   
        assert isinstance(k8scluster_id, string_types), "'k8scluster_id' must be a string"
        assert re.match(r'\/api\/v2\/k8scluster\/[0-9]+', k8scluster_id), "'k8scluster_id' must have format '/api/v2/worker/k8scluster/[0-9]+'"
        assert isinstance(status, list), "'status' must be a list"
        for i, s in enumerate(status):
            assert isinstance(s, K8sClusterStatus), "'status' item '{}' is not of type K8sClusterStatus".format(i)
        assert isinstance(timeout_secs, int), "'timeout_secs' must be an int"   
        assert timeout_secs >= 0, "'timeout_secs' must be >= 0"

        try:
            polling.poll(
                lambda: self.get(k8scluster_id).status in [ s.name for s in status ],
                step=10,
                poll_forever=False,
                timeout=timeout_secs
            )
            return True
        except polling.TimeoutException:
            return False

    def delete(self, k8scluster_id):
        """Delete a K8S Cluster.

        You can use `watch_for_status()` to check for the cluster state/existence.

        Args:
            k8scluster_id: (int) the K8S cluster ID
            
        Raises:
            APIException
        """
        assert isinstance(k8scluster_id, str),"'k8scluster_id' must be provided and must be a string"
        assert re.match(r'\/api\/v2\/k8scluster\/[0-9]+', k8scluster_id), "'k8scluster_id' must have format '/api/v2/worker/k8scluster/[0-9]+'"

        self.client._request(url=k8scluster_id, http_method='delete', description='k8s_cluster/delete')