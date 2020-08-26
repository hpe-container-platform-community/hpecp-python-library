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

import six
from mock import patch

from hpecp import ContainerPlatformClient
from hpecp.exceptions import APIItemNotFoundException

from .base import BaseTestCase, get_client
from .user_mock_api_responses import mockApiSetup

# setup the mock data
mockApiSetup()


class TestUsers(TestCase):
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_users(self, mock_get, mock_post):
        client = ContainerPlatformClient(
            username="admin",
            password="admin123",
            api_host="127.0.0.1",
            api_port=8080,
            use_ssl=True,
        )

        # Makes POST Request: https://127.0.0.1:8080/api/v1/login
        client.create_session()

        # Makes GET Request: https://127.0.0.1:8080/api/v1/user
        users = client.user.list()

        # Test that json response is saved in each WorkerK8s object
        assert users[0].json is not None

        # Test UserList subscriptable access and property setters
        assert users[0].is_service_account is False
        assert users[0].is_siteadmin is False
        assert users[0].default_tenant == ""
        assert users[0].is_external is False
        assert users[0].is_group_added_user is False

        assert users[0].name == "csnow"
        assert users[0].description == "chris"
        assert users[0]._links == {"self": {"href": "/api/v1/user/16"}}


class TestDeleteUser(TestCase):
    @patch("requests.delete", side_effect=BaseTestCase.httpDeleteHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_delete_user(self, mock_post, mock_delete):
        with self.assertRaisesRegexp(
            AssertionError,
            "'id' must be provided and must be a str",
        ):
            get_client().user.delete(id=999)

        with self.assertRaisesRegexp(
            AssertionError,
            "'id' does not start with '/api/v1/user/'",
        ):
            get_client().user.delete(id="garbage")

        with self.assertRaises(APIItemNotFoundException):
            get_client().user.delete(id="/api/v1/user/999")

        get_client().user.delete(id="/api/v1/user/123")


class TestCLI(BaseTestCase):
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_create(self, mock_post):

        hpecp = self.cli.CLI()
        hpecp.user.create(
            name="jdoe",
            password="secret",
            description="Jane Doe",
            is_external=False,
        )

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = "/mock/api/user/1"
        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)
