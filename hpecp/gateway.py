from __future__ import absolute_import
from .logger import Logger
from .exceptions import ContainerPlatformClientException, APIException, APIItemNotFoundException, APIItemConflictException

from operator import attrgetter
from tabulate import tabulate
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
        return [ worker for worker in response.json()["_embedded"]["workers"] if worker['purpose'] == 'proxy' ]

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
                request_url='gateway_id')

        return response.json()

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
        assert re.match(r'\/api\/v1\/workers\/[0-9]+', gateway_id), "'gateway_id' must have format '/api/v1/worker/[0-9]+'"

        # check if host is actually a gateway - raises APIItemNotFoundException() if gateway not found
        self.get(gateway_id)
            
        self.client._request(url=gateway_id, http_method='delete', description='gateway/delete')


    def wait_for_state(self, id, state=[], timeout_secs=60):
        """
        Uses: https://github.com/justiniso/polling/blob/master/polling.py

        status: WorkerK8sStatus value, e.g. WorkerK8sStatus.configured

        raises: Exception
        """
        assert timeout_secs >= 0, "'timeout_secs' must be >= 0"

        try:
            polling.poll(
                lambda: self.get(id)['state'] in state,
                step=10,
                poll_forever=False,
                timeout=timeout_secs
            )
        except polling.TimeoutException:
            message = "Timed out waiting for status: '{}' on Gateway ID: {}".format(state, id)
            self.client.log.error(message)
            raise Exception(message)

        self.client.log.info("Gateway ID: {} was detected to have state {}".format(id, state))

    
    class Gateway():
        pass
    """
    {
        'hacapable': True, 
        'propinfo': 
            {'bds_storage_apollo': 'false', 'bds_network_publicinterface': 'ens5'}, 
        'approved_worker_pubkey': [], 
        'schedule': False, 
        'ip': '10.1.0.37', 
        'proxy_nodes_hostname': 'ec2-35-165-137-87.us-west-2.compute.amazonaws.com', 
        'hostname': 'ip-10-1-0-37.us-west-2.compute.internal', 
        'state': 'installed', 
        '_links': {'self': {'href': '/api/v1/workers/13'}}, 
        'purpose': 'proxy', 
        'status_info': '', 
        'sysinfo': {'network': 
            [{'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '7e:d0:19:00:a1:c0', 'Speed': '10000'}, 'name': 'bds-flood-6-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '52:c4:7b:93:f2:0a', 'Speed': '10000'}, 'name': 'bds-flood-2-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': 'b2:e6:2b:c5:7a:d4', 'Speed': '10000'}, 'name': 'bds-flood-0-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'UNKNOWN', 'Carrier': 'UNKNOWN', 'HwAddr': 'c6:b3:cd:1b:7d:44', 'Speed': 'UNKNOWN'}, 'name': 'bds-flood'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '5a:16:20:0c:d7:f1', 'Speed': '10000'}, 'name': 'bds-flood-1-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': 'c6:bf:e3:af:82:2f', 'Speed': '10000'}, 'name': 'bds-flood-1-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '0e:d9:23:62:96:94', 'Speed': '10000'}, 'name': 'bds-flood-0-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': 'e2:86:7e:62:c0:3c', 'Speed': '10000'}, 'name': 'bds-flood-2-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '8e:92:dc:b9:b7:d7', 'Speed': '10000'}, 'name': 'bds-flood-6-l'}, {'info': {'IsVirtual': False, 'IpAddr': {'dynamic': '10.1.0.37/24'}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '02:72:98:8e:3b:86', 'Speed': 'UNKNOWN'}, 'name': 'ens5'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '2a:4a:c9:c6:d0:28', 'Speed': '10000'}, 'name': 'bds-flood-4-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '7a:22:39:fc:11:7e', 'Speed': '10000'}, 'name': 'bds-flood-5-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '9a:2f:6c:e6:74:30', 'Speed': '10000'}, 'name': 'bds-flood-3-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '7e:ff:e4:5b:56:0d', 'Speed': '10000'}, 'name': 'bds-flood-7-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '4a:f7:7e:95:14:2d', 'Speed': '10000'}, 'name': 'bds-flood-7-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '36:5f:82:61:bf:5c', 'Speed': '10000'}, 'name': 'bds-flood-3-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '6e:86:7d:52:94:5d', 'Speed': '10000'}, 'name': 'bds-flood-5-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': 'e6:24:0f:54:99:a9', 'Speed': '10000'}, 'name': 'bds-flood-4-l'}], 'keys': {'reported_worker_public_key': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDKonffu4vtTSINNpBwvLd367941fhPyEuVfh7KrohdIUSVEh/pX8FDAO9fi9pH979AzdDVWeUclTmktm63vQ39TVIJQ+rqdoZUhtH8rSYFoTFzxUQxONviNJJGTiYYMo4kJsLO1Hk/b9Lz8sxUJWD+e5r2UTM5cDSYT3wBHUCDr/MXAxNC9FAgkpuME5utC1dd1aHj2zgLUP61REjnhy1zVVJnbh/T/y3p8Z5z0ubAQy7pYaMTuWgdVMH6kA/RWzOB2JRj8vFKYp9fysFe7L/nj+C2LkDr4dmMLNL9ffTvpnMOj5qPgAO8bay5hAgVykUaRInLjuL7p5/nFATm9uI4A2a28m4HO9csywNXpm5TBDWPDxW7Wh7Sdkx0xHwZenXXy/em+4Q4Fk4Oc6YwYcKOJVsst0qGeCFkhLjzvFHu2ceYf5Q1gg5FlBiX+LsWngjArsd0sdh+3piH/xFuHdubqHfOFpOlZsQsMX5V/LUA71Wqv/cxMsoD5jybQOUS8o34JjkCZlavuJcIeU4hWlWEliZU5SmppuNkHdosXup20/TyBgg0qYlzc+FKZ/8vlQSjT5WgCNffPgXR94KPF1817RW1YSbR+1oiNg6FXgQrKM/1DiqyQ5D8DjhZWgg33hJ7K/fKCL3qPyWCJEMQ64iLQ4QtSeU46l+aO490A89u6w== server\n'}, 'storage': 
            [{'info': {'IsLogicalVolume': False, 'IsDisk': False, 'Name': '/dev/nvme0n1p1', 'SizeBytes': '429495664128', 'IsReadOnly': False, 'ParentName': '/dev/nvme0n1', 'IsRemovable': False, 'IsRotational': False, 'ParentDeviceType': 'disk', 'IsPartition': True, 'DeviceType': 'part', 'HasFilesystem': True, 'Mountpoint': '/'}, 'name': '/dev/nvme0n1p1'}], 'swap': {'swap_total': 0}, 'memory': {'mem_total': 65842458624}, 'gp': {'gpu_count': 0}, 'cp': {'cpu_logical_cores': 16, 'cpu_count': 8, 'cpu_physical_cores': 8, 'cpu_sockets': 1}, 'mountpoint': []
            }, 
        'tags': []
        }
    """