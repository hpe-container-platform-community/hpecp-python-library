from __future__ import absolute_import
from .logger import Logger

import json
from operator import attrgetter
from tabulate import tabulate
import polling
from enum import Enum
import re

try:
  basestring
except NameError:
  basestring = str

class K8sClusterController:
    """This is the main class that users will interact with to work with K8S Clusters.

    An instance of this class is available in the client.ContainerPlatformClient with the attribute name
    :py:attr:`k8s_cluster <.client.ContainerPlatformClient.k8s_cluster>`.  The methods of this class can be 
    invoked using `client.k8s_cluster.method()`.  See the example below:

    Example::

        client = ContainerPlatformClient(...).create_session()
        client.k8s_cluster.list()

    """

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
        """Send an API request to create a K8s Cluster.  The cluster creation will be asynchronous - use 
        the :py:meth:`wait_for_status` method to wait for the cluster to be created.

        For the lis of statuses see :py:class:`K8sClusterStatus`

        Arguments:

            name: str 
                Cluster name - required parameter.  Name must be at least 1 characters
            description: str
                Cluster description - defaults to empty string if not provided
            k8s_version: str
                Kubernetes version to configure. If not specified defaults to the latest version as supported by the rpms.
            pod_network_range: str
                Network range to be used for kubernetes pods. Defaults to `10.192.0.0/12`
            service_network_range: str
                Network range to be used for kubernetes services that are exposed with Cluster IP. Defaults to `10.96.0.0/12`
            pod_dns_domain: str
                DNS Domain to be used for kubernetes pods. Defaults to `cluster.local`
            persistent_storage_local: str
                Enables local host storage to be available in the kubernetes cluster
            persistent_storage_nimble_csi: bool
                Set to True to installs the Nimble CSI plugin for Nimble storage to be available in the kubernetes cluster
            k8shosts_config: list[K8sClusterHostConfig]
                list of :py:class:`K8sClusterHostConfig` objects determining which hosts to add and their role (master or worker)

        Returns:

            K8s Cluster ID with the format: '/api/v2/k8scluster/[0-9]+'

        Raises:

            APIException
        """

        assert isinstance(name, basestring) and len(name) > 0,"'name' must be provided and must be a string"
        assert description is None or isinstance(description, basestring), "'description' if provided, must be a string"
        assert k8s_version is None or isinstance(k8s_version, basestring), "'k8s_version' if provided, must be a string"
        assert isinstance(pod_network_range, basestring), "'pod_network_range' must be a string"
        assert isinstance(service_network_range, basestring), "'service_network_range' must be a string"
        assert isinstance(pod_dns_domain, basestring), "'pod_dns_domain' must be a string"
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

            :py:class:`K8sClusterList` List of K8s Clusters
            
        Raises:

            APIException
        """
        response = self.client._request(url='/api/v2/k8scluster', http_method='get', description='k8s_cluster/list')
        return K8sClusterList(response.json()['_embedded']['k8sclusters'])

    def get(self, k8scluster_id, setup_log=False):
        """Retrieve a K8S Cluster by ID.

        Args:
            k8scluster_id: str
                The K8S cluster ID - format: '/api/v2/k8scluster/[0-9]+'
            setup_log: (bool) 
                Set to True to return the cluster setup log

        Returns:
            K8sCluster: object representing K8S Cluster
            
        Raises:
            APIException
        """
        assert isinstance(k8scluster_id, str),"'k8scluster_id' must be provided and must be a string"
        assert re.match(r'\/api\/v2\/k8scluster\/[0-9]+', k8scluster_id), "'k8scluster_id' must have format '/api/v2/k8scluster/[0-9]+'"

        if setup_log == True:
            params = '?setup_log'
        else:
            params = ''

        response = self.client._request(url='{}{}'.format(k8scluster_id, params), http_method='get', description='k8s_cluster/get')
        return K8sCluster(response.json())

    def wait_for_status(self, k8scluster_id, status=[], timeout_secs=60):
        """Wait for cluster status.

        Args:
            k8scluster_id: str
                The K8S cluster ID - format: '/api/v2/k8scluster/[0-9]+'
            status: list[:py:class:`K8sClusterStatus`]
                Status(es) to wait for.  Use an empty array if you want to wait for a cluster's existence to cease.
            timeout_secs: int
                How long to wait for the status(es) before raising an exception.

        Returns:
            bool: True if status was found before timeout, otherwise False
            
        Raises:
            APIItemNotFoundException: if the item is not found
            APIException: if a generic API exception occurred
        """
   
        assert isinstance(k8scluster_id, basestring), "'k8scluster_id' must be a string"
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

        You can use :py:meth:`wait_for_status` to check for the cluster state/existence.

        Args:
            k8scluster_id: str
                The K8S cluster ID - format: '/api/v2/k8scluster/[0-9]+'
            
        Raises:
            APIException
        """
        assert isinstance(k8scluster_id, str),"'k8scluster_id' must be provided and must be a string"
        assert re.match(r'\/api\/v2\/k8scluster\/[0-9]+', k8scluster_id), "'k8scluster_id' must have format '/api/v2/worker/k8scluster/[0-9]+'"

        self.client._request(url=k8scluster_id, http_method='delete', description='k8s_cluster/delete')

    def supported_k8s_versions(self):
        """Not yet implemented - see https://github.com/hpe-container-platform-community/hpecp-python-library/issues/3"""
        raise NotImplementedError()

class K8sClusterStatus(Enum):
    """Bases: enum.Enum
    
    The statuses for a K8S Cluster

    **Note:** 
    
    The integer values do not have a meaning outside of this library.  
    The API uses a string identifier with the status name rather than an integer value.
    """

    ready = 1
    creating = 2
    updating = 3
    upgrading = 4
    deleting = 5
    error = 6
    warning = 7


class K8sCluster():
    """Create an instance of K8sCluster from json data returned from the HPE Container Platform API.

    Users of this library are not expected to create an instance of this class.

    Parameters:
        json : str
            The json returned by the API representing a K8sCluster.

    Returns:
        K8sCluster: 
            An instance of K8sCluster
    """

    all_fields = [ 
        'id', 
        'name', 
        'description', 
        'k8s_version', 
        'created_by_user_id', 
        'created_by_user_name', 
        'created_time',
        'k8shosts_config',
        'admin_kube_config',
        'dashboard_token',
        'api_endpoint_access',
        'dashboard_endpoint_access',
        'cert_data',
        'status',
        'status_message',
        '_links'
        ]
    """All of the fields of a K8s Cluster objects that are returned by the HPE Container Platform API"""

    def __init__(self, json):
        self.json = json
        self.display_columns = K8sCluster.all_fields

    def __repr__(self):
        return "<K8sCluster id:{} name:{} description:{} status:{}>".format( self.id, self.name, self.description, self.status)

    def __str__(self):
        return "K8sCluster(id={}, name={}, description={}, status={})".format(
                    self.id, self.name, self.description, self.status)

    def __dir__(self):
        return self.display_columns

    def __getitem__(self, item):
        return getattr(self, self.__dir__()[item])

    def set_display_columns(self, columns):
        """Set the columns this instance should have when the instance is used with :py:meth:`.K8sClusterList.tabulate`

        Parameters:
            columns : list[str]
                Set the list of colums to return

        See :py:attr:`all_fields` for the complete list of field names.
        """
        self.display_columns = columns

    @property
    def id(self): 
        """@Field: from json['_links']['self']['href'] - id format: '/api/v2/k8scluster/[0-9]+'"""
        return self.json['_links']['self']['href']

    @property
    def name(self): 
        """@Field: from json['label']['name']"""
        return self.json['label']['name']

    @property
    def description(self):
        """@Field: from json['label']['description']"""
        return self.json['label']['description']
    
    @property
    def k8s_version(self):
        """@Field: from json['k8s_version']"""
        return self.json['k8s_version']
    
    @property
    def created_by_user_id(self):
        """@Field: from json['created_by_user_id']"""
        return self.json['created_by_user_id']
    
    @property
    def created_by_user_name(self):
        """@Field: from json['created_by_user_name']"""
        return self.json['created_by_user_name']
    
    @property
    def created_time(self):
        """@Field: from json['created_time']"""
        return self.json['created_time']
    
    @property
    def k8shosts_config(self):
        """@Field: from json['k8shosts_config']"""
        return self.json['k8shosts_config']
    
    @property
    def admin_kube_config(self):
        """@Field: from json['admin_kube_config']"""
        if 'admin_kube_config' in self.json:
            return self.json['admin_kube_config']
        else:
            return ''
    
    @property
    def dashboard_token(self):
        """@Field: from json['dashboard_token']"""
        if 'dashboard_token' in self.json:
            return self.json['dashboard_token']
        else:
            return ''
    
    @property
    def api_endpoint_access(self):
        """@Field: from json['api_endpoint_access']"""
        if 'api_endpoint_access' in self.json:
            return self.json['api_endpoint_access']
        else:
            return ''

    @property
    def dashboard_endpoint_access(self):
        """@Field: from json['dashboard_endpoint_access']"""
        if 'dashboard_endpoint_access' in self.json:
            return self.json['dashboard_endpoint_access']
        else:
            return ''
    
    @property
    def cert_data(self):
        """@Field: from json['cert_data'] or None if cert_data not available"""
        try:
            return self.json['cert_data']
        except KeyError:
            return None

    @property
    def status(self):
        """@Field: from json['status']"""
        return self.json['status']

    @property
    def status_message(self):
        """@Field: from json['status_message']"""
        return self.json['status_message']

    @property
    def _links(self):
        """@Field: from json['_links']"""
        return self.json['_links']

    def __len__(self):
        return len(dir(self))

class K8sClusterList():
    """List of :py:obj:`.K8sCluster` objects

    This class is not expected to be instantiated by users.

    Parameters:
        json : str
            json data returned from the HPE Container Platform API get request to /api/v2/k8scluster
    """

    def __init__(self, json):
        self.json = json
        self.clusters = sorted([K8sCluster(t) for t in json],  key=attrgetter('id'))
        self.tenant_columns = K8sCluster.all_fields

    def __getitem__(self, item):
        return self.clusters[item]

    # Python 2
    def next(self):
        """Support iterator access on Python 2.7"""
        if not self.clusters:
           raise StopIteration
        tenant = self.clusters.pop(0)
        tenant.set_display_columns(self.tenant_columns)
        return tenant

    # Python 3
    def __next__(self):
        if not self.clusters:
           raise StopIteration
        tenant = self.clusters.pop(0)
        tenant.set_display_columns(self.tenant_columns)
        return tenant

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.clusters)

    def tabulate(self, columns=K8sCluster.all_fields):
        """Provide a tabular represenation of the list of K8s Clusters

        Parameters:
            columns : list[str]
                list of columns to return in the table - default :py:attr:`.K8sCluster.all_fields`

        Returns:
            str : table output

        Example::

            # Print the cluster list with all of the avaialble fields
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
    """Object to represent a pair of `host node` and the `role` of the host - `master` or `worker`.

    Arguments:

        node: str
            The node ID. Must have. the format: '/api/v2/worker/k8shost/[0-9]+'
        role: str
            The role of the worker node - `master` or `worker`
    """

    @classmethod
    def create_from_list(cls, noderole):
        """Factory method to create K8sClusterHostConfig from a list.
        
        Arguments:
            noderole: list
                the noderole must only have two values: [ node, role ]
        
        See :py:meth:`K8sClusterHostConfig` for the allowed node and role values.
        """

        assert len(noderole) == 2, "'noderole' list must have two values [  node, role ]"
        return K8sClusterHostConfig(node=noderole[0], role=noderole[1])

    def __init__(self, node, role):
        assert isinstance(node, basestring), "'node' must be an string"
        assert re.match(r'\/api\/v2\/worker\/k8shost\/[0-9]+', node), "'node' must have format '/api/v2/worker/k8shost/[0-9]+'"
        assert role in [ 'master', 'worker' ], "'role' must one of ['master, worker']"

        self.node = node
        self.role = role

    def to_dict(self):
        """Returns a dict representation of the object.

        Returns:
            dict

        Example::

            { 
                'node': '/api/v2/worker/k8shost/12', 
                'role': 'master'
            }
        """
        return { 
                'node': self.node, 
                'role': self.role 
            }