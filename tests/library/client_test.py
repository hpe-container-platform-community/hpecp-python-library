from unittest import TestCase
from mock import Mock, patch

import sys
import tempfile
import os
import json
import requests
from requests.exceptions import RequestException
from hpecp import ContainerPlatformClient


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

class TestAuth(TestCase):

    def mocked_requests_get(*args, **kwargs):
        raise RuntimeError("Unhandle POST request: " + args[0]) 

    def mocked_requests_post(*args, **kwargs):
        if args[0] == 'https://127.0.0.1:8080/api/v1/login':
            return MockResponse (
                json_data = { "authorization_endpoint": "https://login.ng.bluemix.net/UAALoginServerWAR"}, 
                status_code = 200,
                headers = { "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71" }
                )
        raise RuntimeError("Unhandle POST request: " + args[0]) 

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('requests.post', side_effect=mocked_requests_post)
    def test_auth(self, mock_get, mock_post):

        client = ContainerPlatformClient(
                                username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True)
        client.create_session()