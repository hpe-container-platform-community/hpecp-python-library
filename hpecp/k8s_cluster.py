from __future__ import absolute_import
from .logger import Logger

import json
from operator import attrgetter
from tabulate import tabulate
import polling
from enum import Enum

import sys
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring


class K8sCluster():
    """
    #TODO add fields
    label required common.label
    Kubernetes cluster name and optional description.

    k8s_version required string
    The version of Kubernetes currently on the cluster. type: string required: true

    created_by_user required string
    The resource path of the EPIC user that submitted the cluster creation.

    created_by_user_name required string
    The name of the EPIC user that submitted the cluster creation. Note that this name is captured at cluster creation submission time and does not track any subsequent user name changes.

    created_time required integer
    Timestamp for cluster submission (in the EPIC platform's timezone). Format is POSIX time.

    k8shosts_config required k8s.k8shost_config []
    List of kubernetes hosts and config information

    admin_kube_config required string
    admin kube config that can be used with kubectl commands

    dashboard_token required string
    base64 encoded token that provides admin access to kubernetes dashboard. Token must be decoded prior to using it with dashboard.

    api_endpoint_access required string
    URL in the form of : specifies endpoint access to kubernetes api server.

    dashboard_endpoint_access required string
    URL in the form of ":" specifies endpoint access to kubernetes dashboard.

    cert_data required string
    The public root CA data provided at install time, if applicable. type: k8scluster_read_certs_obj required: false

    status required, one of (ready, creating, updating, upgrading, deleting, error, warning) string
    Cluster status. Initially this is the status resulting from the launch and configuration of the initial set of nodes. Any future change request that affects the nodes can also change this overall cluster status.

    status_message string
    Brief elaboration on the cluster status. For transient statuses this can contain progress messages. For error/warning statuses, the type of issue.

    _links required common.resource_links
    """

    @staticmethod
    def __class_dir__():
        return [ 'id', 'status', ]

    def __repr__(self):
        return "<ClusterK8S id:{} status:{}>".format( self.id, self.status)

    def __str__(self):
        return "WorkerK8s(id={}, status={})".format(
                    self.id, self.status)

    def __init__(self, json):
        self.json = json
    
    def __dir__(self):
        return K8sCluster.__class_dir__()

    def __getitem__(self, item):
        return getattr(self, self.__dir__()[item])

    @property
    def id(self): return int(self.json['_links']['self']['href'].split('/')[-1])

    @property
    def status(self): return self.json['status']

    def __len__(self):
        return len(dir(self))

class K8sClusterList():

    def __init__(self, json):
        self.json = json
        self.tenants = sorted([K8sCluster(t) for t in json],  key=attrgetter('id'))

    def __getitem__(self, item):
        return self.tenants[item]

    # Python 2
    def next(self):
        if not self.tenants:
           raise StopIteration
        return self.tenants.pop(0)

    # Python 3
    def __next__(self):
        if not self.tenants:
           raise StopIteration
        return self.tenants.pop(0)

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.tenants)

    def tabulate(self):
        return tabulate(self, headers=K8sCluster.__class_dir__(), tablefmt="pretty")


class K8sClusterHostConfig():
    def __init__(self, node_id, node_role):
        assert isinstance(node_id, int), "'node_id' must be an int"
        assert node_role in [ 'master', 'worker' ], "'node_role' must one of ['master, worker']"

        self.node_id = node_id
        self.node_role = node_role

    def to_dict(self):
        return { 
                'node': '/api/v2/worker/k8shost/{}'.format(self.node_id), 
                'role': self.node_role 
            }
        
class K8sClusterController:

    def __init__(self, client):
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
        """Create a K8S Cluster.

        Args:
            name: required, at least 1 characters
            description: defaults to empty string if not provided
            k8s_version: Kubernetes version to configure. If not specified defaults to the latest version as supported by the rpms.
            pod_network_range: Network range to be used for kubernetes pods. Defaults to 10.192.0.0/12
            service_network_range: Network range to be used for kubernetes services that are exposed with Cluster IP. Defaults to 10.96.0.0/12
            pod_dns_domain: DNS Domain to be used for kubernetes pods. Defaults to cluster.local
            persistent_storage_local: Enables local host storage to be available in the kubernetes cluster
            persistent_storage_nimble_csi: Installs the Nimble CSI plugin for Nimble storage to be available in the kubernetes cluster
            k8shosts_config: list of K8sClusterHostConfig objects

        Returns:
            int: The ID for the K8S Cluster
            
        Raises:
            APIException

        """
        assert isinstance(name, string_types) and len(name) > 0,"'name' must be provided and must be a string"
        assert description is None or isinstance(description, string_types), "'description' if provided, must be a string"
        assert k8s_version is None or isinstance(k8s_version, string_types), "'k8s_version' if provided, must be a string"
        assert isinstance(pod_network_range, string_types), "'pod_network_range' must be a string"
        assert isinstance(service_network_range, string_types), "'service_network_range' must be a string"
        assert isinstance(pod_dns_domain, string_types), "'pod_dns_domain' must be a string"
        assert isinstance(persistent_storage_local, bool), "'persistent_storage_local' must be True or False"
        assert isinstance(persistent_storage_nimble_csi, bool), "'persistent_storage_nimble_csi' must be True or False"
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
        return response.headers['Location'].split('/')[-1]

    def list(self):
        """Retrieve list of K8S Clusters.

        Returns:
            K8sClusterList: List of K8s Clusters
            
        Raises:
            APIException

        """
        response = self.client._request(url='/api/v2/k8scluster', http_method='get', description='k8s_cluster/list')
        hosts = K8sClusterList(response.json()['_embedded']['k8sclusters'])
        return hosts

    def get(self, k8scluster_id=None, setup_log=False):
        """Retrieve a K8S Cluster details.

        Args:
            k8scluster_id: (int) the K8S cluster ID
            setup_log: (bool) set to True to return the cluster setup log

        Returns:
            K8sCluster: object representing K8S Cluster
            
        Raises:
            APIException

        """
        if setup_log == True:
            params = '?setup_log'
        else:
            params = ''

        response = self.client._request(url='/api/v2/k8scluster/{}{}'.format(k8scluster_id, params), http_method='get', description='k8s_cluster/list')
        host = K8sCluster(response.json())
        return host