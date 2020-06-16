# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from unittest import TestCase

import requests
from mock import patch

from hpecp import ContainerPlatformClient
from hpecp.exceptions import APIItemNotFoundException


class MockResponse:
    def __init__(
        self,
        json_data,
        status_code,
        headers,
        raise_for_status_flag=False,
        text_data="",
    ):
        self.json_data = json_data
        self.text = text_data
        self.status_code = status_code
        self.raise_for_status_flag = raise_for_status_flag
        self.headers = headers

    def raise_for_status(self):
        if self.raise_for_status_flag:
            self.text = "some error occurred"
            raise requests.exceptions.HTTPError()
        else:
            return

    def json(self):
        return self.json_data


def get_client():
    client = ContainerPlatformClient(
        username="admin",
        password="admin123",
        api_host="127.0.0.1",
        api_port=8080,
        use_ssl=True,
    )
    client.create_session()
    return client


class TestTentants(TestCase):
    def mocked_requests_get(*args, **kwargs):
        print(args[0])
        if args[0] == "https://127.0.0.1:8080/api/v1/tenant":
            return MockResponse(
                # This json data was captured from calling the /tenants api on
                # a clean HPECP 5.0 installation.
                json_data={
                    "_embedded": {
                        "tenants": [
                            {
                                "status": "ready",
                                "features": {
                                    "ml_project": False,
                                    "kubernetes_access": False,
                                },
                                "persistent_supported": True,
                                "member_key_available": "all_admins",
                                "quota": {},
                                "cluster_isolation_supported": True,
                                "inusequota": {
                                    "disk": 0,
                                    "cores": 0,
                                    "memory": 0,
                                    "persistent": 0,
                                    "gpus": 0,
                                },
                                "external_user_groups": [],
                                "gpu_usage_supported": True,
                                "_links": {
                                    "self": {"href": "/api/v1/tenant/1"}
                                },
                                "filesystem_mount_supported": True,
                                "tenant_enforcements": [],
                                "label": {
                                    "name": "Site Admin",
                                    "description": (
                                        "Site Admin Tenant"
                                        " for BlueData clusters"
                                    ),
                                },
                                "constraints_supported": False,
                                "tenant_storage_quota_supported": False,
                            },
                            {
                                "status": "ready",
                                "tenant_type": "docker",
                                "features": {
                                    "ml_project": False,
                                    "kubernetes_access": False,
                                },
                                "persistent_supported": True,
                                "member_key_available": "all_admins",
                                "quota": {},
                                "cluster_isolation_supported": True,
                                "inusequota": {
                                    "disk": 0,
                                    "cores": 0,
                                    "memory": 0,
                                    "persistent": 0,
                                    "gpus": 0,
                                },
                                "external_user_groups": [],
                                "gpu_usage_supported": True,
                                "_links": {
                                    "self": {"href": "/api/v1/tenant/2"}
                                },
                                "filesystem_mount_supported": True,
                                "tenant_enforcements": [],
                                "label": {
                                    "name": "Demo Tenant",
                                    "description": (
                                        "Demo Tenant for BlueData Clusters"
                                    ),
                                },
                                "constraints_supported": True,
                                "tenant_storage_quota_supported": True,
                                "qos_multiplier": 1,
                            },
                        ]
                    },
                    "_links": {"self": {"href": "/api/v1/tenant"}},
                },
                status_code=200,
                headers={},
            )
        if args[0] == "https://127.0.0.1:8080/api/v1/tenant/1":
            # TODO: Get live data for individual tenants
            return MockResponse(
                json_data={
                    "status": "ready",
                    "features": {
                        "ml_project": False,
                        "kubernetes_access": False,
                    },
                    "persistent_supported": True,
                    "member_key_available": "all_admins",
                    "quota": {},
                    "cluster_isolation_supported": True,
                    "inusequota": {
                        "disk": 0,
                        "cores": 0,
                        "memory": 0,
                        "persistent": 0,
                        "gpus": 0,
                    },
                    "external_user_groups": [],
                    "gpu_usage_supported": True,
                    "_links": {"self": {"href": "/api/v1/tenant/1"}},
                    "filesystem_mount_supported": True,
                    "tenant_enforcements": [],
                    "label": {
                        "name": "Site Admin",
                        "description": (
                            "Site Admin Tenant for BlueData clusters"
                        ),
                    },
                    "constraints_supported": False,
                    "tenant_storage_quota_supported": False,
                },
                status_code=200,
                headers={},
            )
        if args[0] == "https://127.0.0.1:8080/api/v1/tenant/2":
            # TODO: Get live data for individual tenants
            return MockResponse(
                json_data={
                    "status": "ready",
                    "tenant_type": "docker",
                    "features": {
                        "ml_project": False,
                        "kubernetes_access": False,
                    },
                    "persistent_supported": True,
                    "member_key_available": "all_admins",
                    "quota": {},
                    "cluster_isolation_supported": True,
                    "inusequota": {
                        "disk": 0,
                        "cores": 0,
                        "memory": 0,
                        "persistent": 0,
                        "gpus": 0,
                    },
                    "external_user_groups": [],
                    "gpu_usage_supported": True,
                    "_links": {"self": {"href": "/api/v1/tenant/2"}},
                    "filesystem_mount_supported": True,
                    "tenant_enforcements": [],
                    "label": {
                        "name": "Demo Tenant",
                        "description": "Demo Tenant for BlueData Clusters",
                    },
                    "constraints_supported": True,
                    "tenant_storage_quota_supported": True,
                    "qos_multiplier": 1,
                },
                status_code=200,
                headers={},
            )
        if args[0] == "https://127.0.0.1:8080/api/v1/tenant/100":
            # TODO: Get live data for individual tenants
            return MockResponse(
                json_data={},
                status_code=404,
                headers={},
                raise_for_status_flag=True,
            )
        raise RuntimeError("Unhandled GET request: " + args[0])

    def mocked_requests_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={
                    "location": (
                        "/api/v1/session/"
                        "df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                    )
                },
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_tenant_list(self, mock_get, mock_post):

        client = get_client()

        # Makes GET Request: https://127.0.0.1:8080/api/v1/tenant
        tenants = client.tenant.list()

        # Test that json response is saved in each Tenant object
        self.assertIsNotNone(client.tenant.list()[0].json)

        # Test TenantList subscriptable access and Tenant property setters
        self.assertEqual(tenants[0].id, "/api/v1/tenant/1")
        self.assertEqual(tenants[0].status, "ready")
        self.assertEqual(tenants[0].name, "Site Admin")
        self.assertEqual(
            tenants[0].description, "Site Admin Tenant for BlueData clusters"
        )

        # Test TenantList iterators
        self.assertEqual(
            [tenant.id for tenant in client.tenant.list()],
            ["/api/v1/tenant/1", "/api/v1/tenant/2"],
        )

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_tenant_id_format(self, mock_get, mock_post):
        client = get_client()

        with self.assertRaisesRegexp(
            AssertionError,
            (
                "'tenant_id' must have format "
                + r"'\/api\/v1\/tenant\/\[0-9\]\+'"  # noqa: W503
            ),
        ):
            client.tenant.get("garbage")

        with self.assertRaisesRegexp(
            AssertionError,
            (
                "'tenant_id' must have format "
                + r"'\/api\/v1\/tenant\/\[0-9\]\+'"  # noqa: W503
            ),
        ):
            client.tenant.get("/api/v1/tenant/some_id")

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_tenant(self, mock_get, mock_post):
        tenant = get_client().tenant.get("/api/v1/tenant/1")
        self.assertEqual(tenant.id, "/api/v1/tenant/1")

        tenant = get_client().tenant.get("/api/v1/tenant/2")
        self.assertEqual(tenant.id, "/api/v1/tenant/2")

        with self.assertRaises(APIItemNotFoundException):
            get_client().tenant.get("/api/v1/tenant/100")
