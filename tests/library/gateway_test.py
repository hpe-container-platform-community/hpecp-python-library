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
        if args[0] == 'https://127.0.0.1:8080/api/v2/k8scluster':
            return MockResponse  (
                json_data = { },
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
    def test_get_gateway(self, mock_get, mock_post):

        with self.assertRaisesRegexp(AssertionError, "'gateway_id' must be provided and must be a string"):
            get_client().gateway.get(123)

        # pylint: disable=anomalous-backslash-in-string 
        with self.assertRaisesRegexp(AssertionError, "'gateway_id' must have format '\/api\/v1\/workers\/\[0-9\]\+'"):
            get_client().gateway.get('garbage')

        # TODO
        # test should return gateway object

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