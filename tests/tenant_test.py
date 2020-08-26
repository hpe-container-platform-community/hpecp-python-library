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

from mock import patch

from hpecp.exceptions import APIItemNotFoundException

from .base import BaseTestCase, get_client
from .tenant_mock_api_responses import mockApiSetup

# setup the mock data
mockApiSetup()


class TestTentants(BaseTestCase):
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
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
        self.assertEqual(tenants[0].tenant_type, "docker")
        self.assertEqual(
            tenants[0].description, "Site Admin Tenant for BlueData clusters"
        )

        # Test TenantList iterators
        self.assertEqual(
            [tenant.id for tenant in client.tenant.list()],
            ["/api/v1/tenant/1", "/api/v1/tenant/2"],
        )

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_tenant_id_format(self, mock_get, mock_post):
        client = get_client()

        with self.assertRaisesRegexp(
            AssertionError,
            ("'id' does not start with '/api/v1/tenant/'"),
        ):
            client.tenant.get("garbage")

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_tenant(self, mock_get, mock_post):
        tenant = get_client().tenant.get("/api/v1/tenant/1")
        self.assertEqual(tenant.id, "/api/v1/tenant/1")

        tenant = get_client().tenant.get("/api/v1/tenant/2")
        self.assertEqual(tenant.id, "/api/v1/tenant/2")

        with self.assertRaises(APIItemNotFoundException):
            get_client().tenant.get("/api/v1/tenant/100")
