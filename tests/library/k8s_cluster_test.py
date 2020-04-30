from unittest import TestCase
from mock import Mock, patch

import sys
import tempfile
import os
import json
import requests
from requests.exceptions import RequestException
from hpecp import ContainerPlatformClient
#from hpecp.k8s_cluster import ClusterK8sStatus


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

class TestClusters(TestCase):

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
    def test_get_k8shosts(self, mock_get, mock_post):

        client = ContainerPlatformClient(
                                username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True)

        # Makes POST Request: https://127.0.0.1:8080/api/v1/login
        client.create_session()

        # Makes GET Request: https://127.0.0.1:8080/api/v2/k8sclusters/
        clusters = client.k8s_cluster.list()

        # Test that json response is saved in each WorkerK8s object
        #assert client.k8s_cluster.get()[0].json is not None

        # Test WorkerK8sList subscriptable access and property setters
        assert clusters[0].id == '/api/v2/k8scluster/20'
        #assert clusters[0].status == ClusterK8sStatus.read.name

        # Test iterators
        #assert [ cluster.id for cluster in client.k8s_cluster.get() ] == [ '/api/v2/k8scluster/20' ]

 


   