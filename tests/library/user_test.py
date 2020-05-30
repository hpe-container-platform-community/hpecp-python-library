from unittest import TestCase
from mock import Mock, patch

import sys
import tempfile
import os
import json
import requests
from requests.exceptions import RequestException
from hpecp import ContainerPlatformClient
from hpecp.k8s_worker import WorkerK8sStatus


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

class TestUsers(TestCase):

    def mocked_requests_get(*args, **kwargs):
        print(args[0])
        if args[0] == 'https://127.0.0.1:8080/api/v1/user/':
            return MockResponse  (
                json_data = 
                    {"_embedded": 
                        {
                            "users": [
                                {
                                    "_links": {
                                    "self": {
                                        "href": "/api/v1/user/16"
                                    }
                                    },
                                    "label": {
                                    "name": "csnow",
                                    "description": "chris"
                                    },
                                    "is_group_added_user": False,
                                    "is_external": False,
                                    "is_service_account": False,
                                    "default_tenant": "",
                                    "is_siteadmin": False
                                },
                                {
                                    "_links": {
                                    "self": {
                                        "href": "/api/v1/user/5"
                                    }
                                    },
                                    "label": {
                                    "name": "admin",
                                    "description": "BlueData Administrator"
                                    },
                                    "is_group_added_user": False,
                                    "is_external": False,
                                    "is_service_account": False,
                                    "default_tenant": "/api/v1/tenant/1",
                                    "is_siteadmin": True
                                }
                            ]
                        }
                    },
                status_code = 200,
                headers = { }
            )
        elif args[0] == 'https://127.0.0.1:8080/api/v1/user/16/':
            return MockResponse  (
                json_data = 
                    {
                        "_links": {
                        "self": {
                            "href": "/api/v1/user/16"
                        }
                        },
                        "label": {
                        "name": "csnow",
                        "description": "chris"
                        },
                        "is_group_added_user": False,
                        "is_external": False,
                        "is_service_account": False,
                        "default_tenant": "",
                        "is_siteadmin": False
                    },
                status_code = 200,
                headers = { }
            )
        else:
            raise RuntimeError("Unhandle GET request: " + args[0]) 

    def mocked_requests_post(*args, **kwargs):
        if args[0] == 'https://127.0.0.1:8080/api/v1/login':
            return MockResponse (
                json_data = { }, 
                status_code = 200,
                headers = { "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71" }
                )
        else:
            raise RuntimeError("Unhandle POST request: " + args[0]) 

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('requests.post', side_effect=mocked_requests_post)
    def test_get_users(self, mock_get, mock_post):

        client = ContainerPlatformClient(
                                username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True)

        # Makes POST Request: https://127.0.0.1:8080/api/v1/login
        client.create_session()

        # Makes GET Request: https://127.0.0.1:8080/api/v1/user
        users = client.user.list()

        # Test that json response is saved in each WorkerK8s object
        assert users[0].json is not None

        # Test UserList subscriptable access and property setters
        assert users[0].is_service_account == False
        assert users[0].is_siteadmin == False
        assert users[0].default_tenant == ''
        assert users[0].is_external == False
        assert users[0].is_group_added_user == False
