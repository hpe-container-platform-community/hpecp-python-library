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

class TestTentants(TestCase):

    def mocked_requests_get(*args, **kwargs):
        if args[0] == 'https://127.0.0.1:8080/api/v1/tenant':
            return MockResponse  (
                #  This json data was captured from calling the /tenants api on a clean HPECP 5.0 installation.
                json_data = 
                    {'_embedded': {'tenants': [
                            {'status': 'ready', 'features': {'ml_project': False, 'kubernetes_access': False}, 'persistent_supported': True, 'member_key_available': 'all_admins', 'quota': {}, 'cluster_isolation_supported': True, 'inusequota': {'disk': 0, 'cores': 0, 'memory': 0, 'persistent': 0, 'gpus': 0}, 'external_user_groups': [], 'gpu_usage_supported': True, '_links': {'self': {'href': '/api/v1/tenant/1'}}, 'filesystem_mount_supported': True, 'tenant_enforcements': [],  'label':  {'name': 'Site Admin', 'description': 'Site Admin Tenant for BlueData clusters'}, 'constraints_supported': False, 'tenant_storage_quota_supported': False},
                            {'status': 'ready', 'tenant_type': 'docker', 'features': {'ml_project': False, 'kubernetes_access': False}, 'persistent_supported': True, 'member_key_available': 'all_admins', 'quota': {}, 'cluster_isolation_supported': True, 'inusequota': {'disk': 0, 'cores': 0, 'memory': 0, 'persistent': 0, 'gpus': 0}, 'external_user_groups': [], 'gpu_usage_supported': True, '_links': {'self': {'href': '/api/v1/tenant/2'}}, 'filesystem_mount_supported': True, 'tenant_enforcements': [], 'label': {'name': 'Demo Tenant', 'description': 'Demo Tenant for BlueData Clusters'}, 'constraints_supported': True, 'tenant_storage_quota_supported': True, 'qos_multiplier': 1}
                        ]}, '_links': {'self': {'href': '/api/v1/tenant'}}},
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
    def test_epic_tenant_list(self, mock_get, mock_post):

        client = ContainerPlatformClient(
                                username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True)
        client.create_session()

        tenants = client.epic_tenant.list()

        assert client.epic_tenant.list()[0].json is not None

        assert tenants[0].tenant_id == 1
        assert tenants[0].status == 'ready'
        assert tenants[0].name == 'Site Admin'
        assert tenants[0].description == 'Site Admin Tenant for BlueData clusters'



   