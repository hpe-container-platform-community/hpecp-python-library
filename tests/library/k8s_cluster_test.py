from unittest import TestCase
from mock import Mock, patch

import sys
import tempfile
import os
import json
import requests
from requests.exceptions import RequestException
from hpecp import ContainerPlatformClient, APIException
from hpecp.k8s_cluster import K8sClusterHostConfig


class MockResponse:
    def __init__(self, json_data, status_code, headers, raise_for_status_flag=False, text_data='', ):
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

class TestClusterList(TestCase):

    def mocked_requests_get(*args, **kwargs):
        if args[0] == 'https://127.0.0.1:8080/api/v2/k8scluster':
            return MockResponse  (
                json_data = {  
                    "_links": {"self": {"href": "/api/v2/k8scluster"}}, 
                    "_embedded": {
                        "k8sclusters": [
                            {
                                "_links": {"self": {"href": "/api/v2/k8scluster/20"}}, 
                                "label": {"name": "def", "description": "my cluster"}, 
                                "k8s_version": "1.17.0", 
                                "pod_network_range": "10.192.0.0/12", 
                                "service_network_range": "10.96.0.0/12", 
                                "pod_dns_domain": "cluster.local", 
                                "created_by_user_id": "/api/v1/user/5", 
                                "created_by_user_name": "admin", 
                                "created_time": 1588260014, 
                                "k8shosts_config": [
                                    {"node": "/api/v2/worker/k8shost/4", "role": "worker"}, 
                                    {"node": "/api/v2/worker/k8shost/5", "role": "master"}
                                ], 
                                "status": "ready", 
                                "status_message": "", 
                                "api_endpoint_access": "https://ip-10-1-0-48.eu-west-2.compute.internal:10002", 
                                "dashboard_endpoint_access": "https://ip-10-1-0-48.eu-west-2.compute.internal:10000", 
                                "admin_kube_config": "apiVersion: v1\nclusters:\n- cluster:\n    certificate-authority-data: xyz=\n    server: https://ip-10-1-0-48.eu-west-2.compute.internal:10002\n  name: k8s-20\ncontexts:\n- context:\n    cluster: k8s-20\n    user: kubernetes-admin\n  name: kubernetes-admin@k8s-20\ncurrent-context: kubernetes-admin@k8s-20\nkind: Config\npreferences: {}\nusers:\n- name: kubernetes-admin\n  user:\n    client-certificate-data: 123=\n    client-key-data: def=", 
                                "dashboard_token": "abc==", 
                                "persistent_storage": {"nimble_csi": False}
                            }
                        ]}},
                status_code = 200,
                headers = { }
            )
        raise RuntimeError("Unhandle GET request: " + args[0]) 

    def mocked_requests_post(*args, **kwargs):
        if args[0] == 'https://127.0.0.1:8080/api/v1/login':
            return MockResponse (
                json_data = { }, 
                status_code = 200,
                headers = { "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71" }
                )
        raise RuntimeError("Unhandle POST request: " + args[0]) 

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('requests.post', side_effect=mocked_requests_post)
    def test_get_k8sclusters(self, mock_get, mock_post):

        # Makes GET Request: https://127.0.0.1:8080/api/v2/k8sclusters/
        clusters = get_client().k8s_cluster.list()

        # Test that json response is saved in each WorkerK8s object
        #assert client.k8s_cluster.get()[0].json is not None

        # Test WorkerK8sList subscriptable access and property setters
        assert clusters[0].id == '/api/v2/k8scluster/20'
        #assert clusters[0].status == ClusterK8sStatus.read.name

        # Test iterators
        assert [ cluster.id for cluster in get_client().k8s_cluster.list() ] == [ '/api/v2/k8scluster/20' ]

        self.maxDiff = None
        self.assertEqual(
            clusters.tabulate(), 
            "+-----------------------+------+-------------+-------------+--------------------+----------------------+--------------+--------+\n" +
            "|          id           | name | description | k8s_version | created_by_user_id | created_by_user_name | created_time | status |\n" +
            "+-----------------------+------+-------------+-------------+--------------------+----------------------+--------------+--------+\n" +
            "| /api/v2/k8scluster/20 | def  | my cluster  |   1.17.0    |   /api/v1/user/5   |        admin         |  1588260014  | ready  |\n" +
            "+-----------------------+------+-------------+-------------+--------------------+----------------------+--------------+--------+"
        )

class TestCreateCluster(TestCase):

    def mocked_requests_create_post(*args, **kwargs):
        if args[0] == 'https://127.0.0.1:8080/api/v1/login':
            return MockResponse (
                json_data = { }, 
                status_code = 200,
                headers = { "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71" }
                )
        elif args[0] == 'https://127.0.0.1:8080/api/v2/k8scluster':
            return MockResponse (
                json_data = { }, 
                status_code = 200,
                headers = { "Location": "/api/v2/k8sclusters/99" }
                ) 
        raise RuntimeError("Unhandle POST request: " + args[0]) 

    @patch('requests.post', side_effect=mocked_requests_create_post)
    def test_create(self, mock_post):

        with self.assertRaisesRegex(AssertionError, "'name' must be provided and must be a string"):
            get_client().k8s_cluster.create()

        with self.assertRaisesRegex(AssertionError, "'description' if provided, must be a string"):
            get_client().k8s_cluster.create(name='a', description=1)
 
        with self.assertRaisesRegex(AssertionError, "'k8s_version' if provided, must be a string"):
            get_client().k8s_cluster.create(name='a', k8s_version=1)
   
        with self.assertRaisesRegex(AssertionError, "'pod_network_range' must be a string"):
            get_client().k8s_cluster.create(name='a', pod_network_range=1)

        with self.assertRaisesRegex(AssertionError, "'service_network_range' must be a string"):
            get_client().k8s_cluster.create(name='a', service_network_range=1)

        with self.assertRaisesRegex(AssertionError, "'pod_dns_domain' must be a string"):
            get_client().k8s_cluster.create(name='a', pod_dns_domain=1)

        with self.assertRaisesRegex(AssertionError, "'persistent_storage_local' must be True or False"):
            get_client().k8s_cluster.create(name='a', persistent_storage_local=1)
        
        with self.assertRaisesRegex(AssertionError, "'persistent_storage_nimble_csi' must be True or False"):
            get_client().k8s_cluster.create(name='a', persistent_storage_nimble_csi=1)

        with self.assertRaisesRegex(AssertionError, "'k8shosts_config' must be a list"):
            get_client().k8s_cluster.create(name='a', k8shosts_config=1)

        with self.assertRaisesRegex(AssertionError, "'k8shosts_config' must have at least one item"):
            get_client().k8s_cluster.create(name='a', k8shosts_config=[])

        with self.assertRaisesRegex(AssertionError, "'k8shosts_config' item '0' is not of type K8sClusterHostConfig"):
            get_client().k8s_cluster.create(name='a', k8shosts_config=[ 1, 2 ])

        with self.assertRaisesRegex(AssertionError, "'node' must have format '\/api\/v2\/worker\/k8shost\/\[0-9\]\+'"):
            get_client().k8s_cluster.create(name='a', k8shosts_config=[ K8sClusterHostConfig('a', 'b') ])

        with self.assertRaisesRegex(AssertionError, "'role' must one of \['master, worker'\]"):
            get_client().k8s_cluster.create(name='a', k8shosts_config=[ K8sClusterHostConfig('/api/v2/worker/k8shost/1', 'b') ])

        # Finally we can create a cluster 
        id = get_client().k8s_cluster.create(name='a', k8shosts_config=[ K8sClusterHostConfig('/api/v2/worker/k8shost/1', 'master') ])
        self.assertEqual(id, '/api/v2/k8sclusters/99')

    def mocked_requests_create_error_post(*args, **kwargs):
        if args[0] == 'https://127.0.0.1:8080/api/v1/login':
            return MockResponse (
                json_data = { }, 
                status_code = 200,
                headers = { "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71" }
                )
        elif args[0] == 'https://127.0.0.1:8080/api/v2/k8scluster':
            return MockResponse (
                json_data = { }, 
                raise_for_status_flag = True,
                status_code = 500,
                headers = {}
                ) 
        raise RuntimeError("Unhandle POST request: " + args[0]) 

    @patch('requests.post', side_effect=mocked_requests_create_error_post)
    def test_create_with_APIException(self, mock_post):

        with self.assertRaises(APIException):
            get_client().k8s_cluster.create(name='a', k8shosts_config=[ K8sClusterHostConfig('/api/v2/worker/k8shost/1', 'master') ])
