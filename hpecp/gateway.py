from __future__ import absolute_import
from .logger import Logger
from .exceptions import ContainerPlatformClientException, APIException, APIItemNotFoundException, APIItemConflictException

import json
from operator import attrgetter
from tabulate import tabulate
from enum import Enum
import polling
import re

try:
  basestring
except NameError:
  basestring = str

class GatewayController:

    def __init__(self, client):
        self.client = client

    def create_with_ssh_password(self, username, password):
        """Not Implemented yet"""
        raise NotImplementedError()

    def create_with_ssh_key(self, ip, proxy_node_hostname, ssh_key_data, tags=[]):
        '''Create a gateway instance using SSH key credentials to access the host

        Args:
            ip: str
                TODO
            proxy_node_hostname: str
                TODO
            ssh_key_data: str
                TODO
            tags: list[str]
                TODO

        Returns: gateway ID
        '''

        assert isinstance(ip, basestring), "'ip' must be provided and must be a string"
        assert isinstance(proxy_node_hostname, basestring), "'proxy_node_hostname' must be provided and must be a string"
        assert isinstance(ssh_key_data, basestring), "'ssh_key_data' must be provided and must be a string"

        data = {
                "ip": ip,
                "credentials": {
                    "type": "ssh_key_access",
                    "ssh_key_data": ssh_key_data
                },
                "tags": tags,
                "proxy_nodes_hostname": proxy_node_hostname,
                "purpose": "proxy"
            }

        response = self.client._request(url='/api/v1/workers/', http_method='post', data=data, description='gateway/create_with_ssh_key')
        return response.headers['location']

    def list(self):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/api/v1/workers/', http_method='get', description='gateway/list')
        return GatewayList(response.json()['_embedded']['workers'])
        

    def get(self, gateway_id):
        """Retrieve a Gateway by ID.

        Args:
            gateway_id: str
                The gateway ID - format: '/api/v1/workers/[0-9]+'

        Returns:
            Gateway: object representing Gateway
            
        Raises:
            APIException
        """
        assert isinstance(gateway_id, str),"'gateway_id' must be provided and must be a string"
        assert re.match(r'\/api\/v1\/workers\/[0-9]+', gateway_id), "'gateway_id' must have format '/api/v1/workers/[0-9]+'"

        response = self.client._request(url=gateway_id, http_method='get', description='gateway/get')
        if response.json()['purpose'] != 'proxy':
            raise APIItemNotFoundException(
                message='gateway not found with id: ' + gateway_id,
                request_method='get',
                request_url=gateway_id)

        return Gateway(response.json())

    def delete(self, gateway_id):
        """Delete a Gateway.

        You can use :py:meth:`wait_for_status` to check for the gateway state/existence.

        Args:
            gateway_id: str
                The Gateway ID - format: '/api/v1/workers/[0-9]+'
            
        Raises:
            APIException
        """
        assert isinstance(gateway_id, str),"'gateway_id' must be provided and must be a string"
        assert re.match(r'\/api\/v1\/workers\/[0-9]+', gateway_id), "'gateway_id' must have format '/api/v1/workers/[0-9]+'"

        # check if host is actually a gateway - raises APIItemNotFoundException() if gateway not found
        self.get(gateway_id)
            
        self.client._request(url=gateway_id, http_method='delete', description='gateway/delete')


    def wait_for_state(self, gateway_id, state=[], timeout_secs=60):
        """Wait for gateway state.

        Args:
            gateway_id: str
                The gateway ID - format: '/api/v1/workers/[0-9]+'
            status: list[:py:class:`GatewayStatus`]
                Status(es) to wait for.  Use an empty array if you want to wait for a cluster's existence to cease.
            timeout_secs: int
                How long to wait for the status(es) before raising an exception.

        Returns:
            bool: True if status was found before timeout, otherwise False
            
        Raises:
            APIItemNotFoundException: if the item is not found
            APIException: if a generic API exception occurred
        """
        assert isinstance(gateway_id, basestring), "'gateway_id' must be a string"
        assert re.match(r'\/api\/v1\/workers\/[0-9]+', gateway_id), "'gateway_id' must have format '/api/v1/workers/[0-9]+'"
        assert isinstance(state, list), "'state' must be a list"
        for i, s in enumerate(state):
            assert isinstance(s, GatewayStatus), "'state' item '{}' is not of type GatewayStatus".format(i)
        assert isinstance(timeout_secs, int), "'timeout_secs' must be an int"   
        assert timeout_secs >= 0, "'timeout_secs' must be >= 0"

        try:
            polling.poll(
                lambda: self.get(gateway_id).state in [ s.name for s in state ],
                step=10,
                poll_forever=False,
                timeout=timeout_secs
            )
            return True
        except polling.TimeoutException:
            return False

class GatewayStatus(Enum):
    """Bases: enum.Enum
    
    The statuses for a Gateway

    **Note:** 
    
    The integer values do not have a meaning outside of this library.  
    The API uses a string identifier with the status name rather than an integer value.
    """

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


class Gateway():
    """Create an instance of Gateway from json data returned from the HPE Container Platform API.

    Users of this library are not expected to create an instance of this class.

    Parameters:
        json : str
            The json returned by the API representing a Gateway.

    Returns:
        Gateway: 
            An instance of Gateway
    """

    all_fields = [ 
        'id',
        'hacapable',
        'propinfo',
        'approved_worker_pubkey',
        'schedule',
        'ip',
        'proxy_nodes_hostname',
        'hostname',
        'state',
        'status_info',
        'purpose',
        'sysinfo',
        'tags'
        ]
    """All of the fields of Gateway objects that are returned by the HPE Container Platform API"""

    default_display_fields = [
        'id',
        'ip',
        'proxy_nodes_hostname',
        'hostname',
        'state',
        'status_info',
        'purpose',
        'tags'
    ]

    def __init__(self, json):
        self.json = json
        self.display_columns = Gateway.default_display_fields

    def __repr__(self):
        return "<Gateway id:{} state:{}>".format( self.id, self.state)

    def __str__(self):
        return "K8sCluster(id={}, state={})".format(self.id, self.state)

    def __dir__(self):
        return self.display_columns

    def __getitem__(self, item):
        return getattr(self, self.display_columns[item])

    def __len__(self):
        return len(dir(self))

    def set_display_columns(self, columns):
        """Set the columns this instance should have when the instance is used with :py:meth:`.GatewayList.tabulate`

        Parameters:
            columns : list[str]
                Set the list of colums to return

        See :py:attr:`all_fields` for the complete list of field names.
        """
        self.display_columns = columns

    @property
    def id(self): 
        """@Field: from json['_links']['self']['href'] - id format: '/api/v1/workers/[0-9]+'"""
        return self.json['_links']['self']['href']

    @property
    def state(self): 
        """@Field: from json['state']"""
        return self.json['state']

    @property
    def hacapable(self): 
        """@Field: from json['hacapable']"""
        return self.json['hacapable']

    @property
    def propinfo(self): 
        """@Field: from json['propinfo']"""
        return self.json['propinfo']

    @property
    def approved_worker_pubkey(self): 
        """@Field: from json['approved_worker_pubkey']"""
        return self.json['approved_worker_pubkey']

    @property
    def schedule(self): 
        """@Field: from json['schedule']"""
        return self.json['schedule']

    @property
    def ip(self): 
        """@Field: from json['ip']"""
        return self.json['ip']

    @property
    def proxy_nodes_hostname(self): 
        """@Field: from json['proxy_nodes_hostname']"""
        return self.json['proxy_nodes_hostname']

    @property
    def hostname(self): 
        """@Field: from json['hostname']"""
        return self.json['hostname']

    @property
    def purpose(self): 
        """@Field: from json['purpose']"""
        return self.json['purpose']

    @property
    def status_info(self): 
        """@Field: from json['status_info']"""
        return self.json['status_info']

    @property
    def sysinfo(self): 
        """@Field: from json['sysinfo']"""
        return self.json['sysinfo']

    @property
    def tags(self): 
        """@Field: from json['tags']"""
        return self.json['tags']

    @property
    def _links(self):
        """@Field: from json['_links']"""
        return self.json['_links']

class GatewayList():
    """List of :py:obj:`.Gateway` objects

    This class is not expected to be instantiated by users.

    Parameters:
        json : str
            json data returned from the HPE Container Platform API get request to /api/v1/Gateway
    """

    def __init__(self, json):
        self.json = [ g for g in json if g['purpose'] == 'proxy']
        self.gateways = sorted([Gateway(g) for g in json if g['purpose'] == 'proxy'], key=attrgetter('id'))
        self.display_columns = Gateway.default_display_fields

    def __getitem__(self, item):
        return self.gateways[item]

    # Python 2
    def next(self):
        """Support iterator access on Python 2.7"""
        if not self.gateways:
           raise StopIteration
        gateway = self.gateways.pop(0)
        gateway.set_display_columns(self.display_columns)
        return gateway

    # Python 3
    def __next__(self):
        if not self.gateways:
           raise StopIteration
        gateway = self.gateways.pop(0)
        gateway.set_display_columns(self.display_columns)
        return gateway

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.gateways)

    def tabulate(self, columns=Gateway.default_display_fields):
        """Provide a tabular represenation of the list of Gateways

        Parameters:
            columns : list[str]
                list of columns to return in the table - default :py:attr:`.Gateway.default_display_fields`

        Returns:
            str : table output

        Example::

            # Print the gateway list with all of the avaialble fields
            print(hpeclient.gateway.list().tabulate())

            # Print the cluster list with a subset of the fields
            print(hpeclient.gateway.list().tabulate(columns=['id', 'state']))
        """
        if columns != Gateway.default_display_fields:
            assert isinstance(columns, list), "'columns' parameter must be list"
            for column in columns:
                assert column in Gateway.all_fields, "item '{}' is not a field in Gateway.all_fields".format(column)

        self.display_columns = columns

        # FIXME https://github.com/hpe-container-platform-community/hpecp-python-library/issues/5
        return tabulate(self, headers=sorted(columns), tablefmt="pretty")
