from unittest import TestCase
from mock import Mock, patch

import sys
import tempfile
import os
import json
import requests
from requests.exceptions import RequestException
from hpecp import ContainerPlatformClient, APIException, APIItemNotFoundException
from hpecp.k8s_cluster import K8sClusterHostConfig, K8sClusterStatus


class MockResponse:
    def __init__(self, json_data, status_code, headers, raise_for_status_flag=False, text_data=''):
        self.json_data = json_data
        self.text = text_data
        self.status_code = status_code
        self.raise_for_status_flag = raise_for_status_flag
        self.headers = headers
    def raise_for_status(self):
        if self.raise_for_status_flag:
            self.text = 'some error occurred'
            raise requests.exceptions.HTTPError()
        else:
            return
    def json(self):
        return self.json_data

def get_client():
        client = ContainerPlatformClient(
                                username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True)
        client.create_session()
        return client

def session_mock_response():
    return MockResponse (
                json_data = { }, 
                status_code = 200,
                headers = { "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71" }
                )

class TestGatewayGet(TestCase):

    # pylint: disable=no-method-argument 
    def mocked_requests_get(*args, **kwargs):
        if args[0] == 'https://127.0.0.1:8080/api/v1/workers/99':
            return MockResponse  (
                json_data = {
                        'hacapable': True, 
                        'propinfo': 
                            {'bds_storage_apollo': 'false', 'bds_network_publicinterface': 'ens5'}, 
                        'approved_worker_pubkey': [], 
                        'schedule': False, 
                        'ip': '10.1.0.37', 
                        'proxy_nodes_hostname': 'ec2-35-165-137-87.us-west-2.compute.amazonaws.com', 
                        'hostname': 'ip-10-1-0-37.us-west-2.compute.internal', 
                        'state': 'installed', 
                        '_links': {'self': {'href': '/api/v1/workers/99'}}, 
                        'purpose': 'proxy', 
                        'status_info': '', 
                        'sysinfo': {'network': 
                            [{'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '7e:d0:19:00:a1:c0', 'Speed': '10000'}, 'name': 'bds-flood-6-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '52:c4:7b:93:f2:0a', 'Speed': '10000'}, 'name': 'bds-flood-2-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': 'b2:e6:2b:c5:7a:d4', 'Speed': '10000'}, 'name': 'bds-flood-0-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'UNKNOWN', 'Carrier': 'UNKNOWN', 'HwAddr': 'c6:b3:cd:1b:7d:44', 'Speed': 'UNKNOWN'}, 'name': 'bds-flood'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '5a:16:20:0c:d7:f1', 'Speed': '10000'}, 'name': 'bds-flood-1-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': 'c6:bf:e3:af:82:2f', 'Speed': '10000'}, 'name': 'bds-flood-1-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '0e:d9:23:62:96:94', 'Speed': '10000'}, 'name': 'bds-flood-0-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': 'e2:86:7e:62:c0:3c', 'Speed': '10000'}, 'name': 'bds-flood-2-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '8e:92:dc:b9:b7:d7', 'Speed': '10000'}, 'name': 'bds-flood-6-l'}, {'info': {'IsVirtual': False, 'IpAddr': {'dynamic': '10.1.0.37/24'}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '02:72:98:8e:3b:86', 'Speed': 'UNKNOWN'}, 'name': 'ens5'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '2a:4a:c9:c6:d0:28', 'Speed': '10000'}, 'name': 'bds-flood-4-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '7a:22:39:fc:11:7e', 'Speed': '10000'}, 'name': 'bds-flood-5-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '9a:2f:6c:e6:74:30', 'Speed': '10000'}, 'name': 'bds-flood-3-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '7e:ff:e4:5b:56:0d', 'Speed': '10000'}, 'name': 'bds-flood-7-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '4a:f7:7e:95:14:2d', 'Speed': '10000'}, 'name': 'bds-flood-7-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '36:5f:82:61:bf:5c', 'Speed': '10000'}, 'name': 'bds-flood-3-r'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': '6e:86:7d:52:94:5d', 'Speed': '10000'}, 'name': 'bds-flood-5-l'}, {'info': {'IsVirtual': True, 'IpAddr': {}, 'Mt': 9001, 'State': 'up', 'Carrier': True, 'HwAddr': 'e6:24:0f:54:99:a9', 'Speed': '10000'}, 'name': 'bds-flood-4-l'}], 'keys': {'reported_worker_public_key': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDKonffu4vtTSINNpBwvLd367941fhPyEuVfh7KrohdIUSVEh/pX8FDAO9fi9pH979AzdDVWeUclTmktm63vQ39TVIJQ+rqdoZUhtH8rSYFoTFzxUQxONviNJJGTiYYMo4kJsLO1Hk/b9Lz8sxUJWD+e5r2UTM5cDSYT3wBHUCDr/MXAxNC9FAgkpuME5utC1dd1aHj2zgLUP61REjnhy1zVVJnbh/T/y3p8Z5z0ubAQy7pYaMTuWgdVMH6kA/RWzOB2JRj8vFKYp9fysFe7L/nj+C2LkDr4dmMLNL9ffTvpnMOj5qPgAO8bay5hAgVykUaRInLjuL7p5/nFATm9uI4A2a28m4HO9csywNXpm5TBDWPDxW7Wh7Sdkx0xHwZenXXy/em+4Q4Fk4Oc6YwYcKOJVsst0qGeCFkhLjzvFHu2ceYf5Q1gg5FlBiX+LsWngjArsd0sdh+3piH/xFuHdubqHfOFpOlZsQsMX5V/LUA71Wqv/cxMsoD5jybQOUS8o34JjkCZlavuJcIeU4hWlWEliZU5SmppuNkHdosXup20/TyBgg0qYlzc+FKZ/8vlQSjT5WgCNffPgXR94KPF1817RW1YSbR+1oiNg6FXgQrKM/1DiqyQ5D8DjhZWgg33hJ7K/fKCL3qPyWCJEMQ64iLQ4QtSeU46l+aO490A89u6w== server\n'}, 'storage': 
                            [{'info': {'IsLogicalVolume': False, 'IsDisk': False, 'Name': '/dev/nvme0n1p1', 'SizeBytes': '429495664128', 'IsReadOnly': False, 'ParentName': '/dev/nvme0n1', 'IsRemovable': False, 'IsRotational': False, 'ParentDeviceType': 'disk', 'IsPartition': True, 'DeviceType': 'part', 'HasFilesystem': True, 'Mountpoint': '/'}, 'name': '/dev/nvme0n1p1'}], 'swap': {'swap_total': 0}, 'memory': {'mem_total': 65842458624}, 'gp': {'gpu_count': 0}, 'cp': {'cpu_logical_cores': 16, 'cpu_count': 8, 'cpu_physical_cores': 8, 'cpu_sockets': 1}, 'mountpoint': []
                            }, 
                        'tags': []
                        },
                status_code = 200,
                headers = { }
            )
        raise RuntimeError("Unhandle GET request: " + args[0]) 

    def mocked_requests_post(*args, **kwargs):
        if args[0] == 'https://127.0.0.1:8080/api/v1/login':
            return session_mock_response()
        raise RuntimeError("Unhandle POST request: " + args[0]) 

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('requests.post', side_effect=mocked_requests_post)
    def test_get_gateway_assertions(self, mock_get, mock_post):

        with self.assertRaisesRegexp(AssertionError, "'gateway_id' must be provided and must be a string"):
            get_client().gateway.get(123)

        # pylint: disable=anomalous-backslash-in-string 
        with self.assertRaisesRegexp(AssertionError, "'gateway_id' must have format '\/api\/v1\/workers\/\[0-9\]\+'"):
            get_client().gateway.get('garbage')

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('requests.post', side_effect=mocked_requests_post)
    def test_get_gateway(self, mock_get, mock_post):

        gateway = get_client().gateway.get('/api/v1/workers/99')

        self.assertEqual(gateway.id, '/api/v1/workers/99')

        # TODO test other property accessors

class TestCreateGateway(TestCase):

    # pylint: disable=no-method-argument 
    def mocked_requests_create_post(*args, **kwargs):
        if args[0] == 'https://127.0.0.1:8080/api/v1/login':
            return session_mock_response()
        elif args[0] == 'https://127.0.0.1:8080/api/v1/workers':
            return MockResponse (
                json_data = { }, 
                status_code = 200,
                headers = { "Location": "/api/v2/workers/99" }
                ) 
        raise RuntimeError("Unhandle POST request: " + args[0]) 

    @patch('requests.post', side_effect=mocked_requests_create_post)
    def test_create_with_ssh_key_assertions(self, mock_post):

        with self.assertRaisesRegexp(AssertionError, "'ip' must be provided and must be a string"):
            get_client().gateway.create_with_ssh_key(
                                                ip=123, 
                                                proxy_node_hostname='my.host.name', 
                                                ssh_key_data='pem encoded key data'
                                                )

        # TODO add more assertions         

    @patch('requests.post', side_effect=mocked_requests_create_post)
    def test_create_with_ssh_key_returns_id(self, mock_post):

        # TODO
        pass