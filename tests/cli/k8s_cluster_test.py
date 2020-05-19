from unittest import TestCase
from mock import Mock, patch, mock_open

from textwrap import dedent
import sys
import tempfile
import os
import json
import requests
from requests.exceptions import RequestException

sys.path.insert(0, os.path.abspath('../../')) 
from bin import cli

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

class TestCLI(TestCase):

    # pylint: disable=no-method-argument 
    def mocked_requests_post(*args, **kwargs):
        if args[0] == 'https://127.0.0.1:8080/api/v1/login':
            return MockResponse (
                json_data = { }, 
                status_code = 200,
                headers = { "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71" }
                )
        raise RuntimeError("Unhandle POST request: " + args[0]) 

    # pylint: disable=no-method-argument 
    def mocked_requests_get(*args, **kwargs ):
        if args[0] == 'http://localhost:8080/api/v2/k8smanifest':
            return MockResponse  (
                json_data = {
                    "_version":"1.0",
                    "supported_versions":[
                        "1.14.10","1.15.7","1.16.4","1.17.0","1.18.0"
                        ],
                    "version_info":{
                        "1.14.10":{"_version":"1.0","min_upgrade_version":"1.13.0","relnote_url":"https://v1-14.docs.kubernetes.io/docs/setup/release/notes/","hpecsi":"1.14"},
                        "1.15.7":{"_version":"1.0","min_upgrade_version":"1.14.0","relnote_url":"https://v1-15.docs.kubernetes.io/docs/setup/release/notes/","hpecsi":"1.15"},
                        "1.16.4":{"_version":"1.0","min_upgrade_version":"1.15.0","relnote_url":"https://v1-16.docs.kubernetes.io/docs/setup/release/notes/","hpecsi":"1.16"},
                        "1.17.0":{"_version":"1.0","min_upgrade_version":"1.16.0","relnote_url":"https://v1-17.docs.kubernetes.io/docs/setup/release/notes/","hpecsi":"1.17"},
                        "1.18.0":{"_version":"1.0","min_upgrade_version":"1.17.0","relnote_url":"https://kubernetes.io/docs/setup/release/notes/","hpecsi":"1.18"}
                        }
                    },
                status_code = 404,
                raise_for_status_flag = True,
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

    @patch('requests.post', side_effect=mocked_requests_post)
    @patch('requests.get', side_effect=mocked_requests_get)
    def test_k8s_supported_versions(self, mock_post, mock_get):
        
        file_data = dedent("""[default]
                        api_host = 127.0.0.1
                        api_port = 8080
                        use_ssl = True
                        verify_ssl = False
                        warn_ssl = True
                        username = admin
                        password = admin123""")

        tmp = tempfile.NamedTemporaryFile(delete=True)
        try:
            tmp.write(file_data.encode('utf-8'))
            tmp.flush()

            cli.HPECP_CONFIG_FILE = tmp.name

            hpecp = cli.CLI()
            hpecp.k8scluster.k8s_supported_versions()

            self.assertTrue(True)

        finally:
            tmp.close()
        