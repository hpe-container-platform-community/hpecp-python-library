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

from .base_test import BaseTestCase, MockResponse, mocked_login_post


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


class TestUsers(TestCase):
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/user/":
            return MockResponse(
                json_data={
                    "_embedded": {
                        "users": [
                            {
                                "_links": {
                                    "self": {"href": "/api/v1/user/16"}
                                },
                                "label": {
                                    "name": "csnow",
                                    "description": "chris",
                                },
                                "is_group_added_user": False,
                                "is_external": False,
                                "is_service_account": False,
                                "default_tenant": "",
                                "is_siteadmin": False,
                            },
                            {
                                "_links": {"self": {"href": "/api/v1/user/5"}},
                                "label": {
                                    "name": "admin",
                                    "description": "BlueData Administrator",
                                },
                                "is_group_added_user": False,
                                "is_external": False,
                                "is_service_account": False,
                                "default_tenant": "/api/v1/tenant/1",
                                "is_siteadmin": True,
                            },
                        ]
                    }
                },
                status_code=200,
                headers={},
            )
        elif args[0] == "https://127.0.0.1:8080/api/v1/user/16/":
            return MockResponse(
                json_data={
                    "_links": {"self": {"href": "/api/v1/user/16"}},
                    "label": {"name": "csnow", "description": "chris"},
                    "is_group_added_user": False,
                    "is_external": False,
                    "is_service_account": False,
                    "default_tenant": "",
                    "is_siteadmin": False,
                },
                status_code=200,
                headers={},
            )
        else:
            raise RuntimeError("Unhandle GET request: " + args[0])

    def mocked_requests_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={
                    "location": (
                        "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                    )
                },
            )
        else:
            raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
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
    # pylint: disable=no-method-argument
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/user/123":
            return MockResponse(
                json_data={
                    "_links": {"self": {"href": "/api/v1/user/123"}},
                    "purpose": "proxy",
                },
                status_code=200,
                headers={},
            )
        if args[0] == "https://127.0.0.1:8080/api/v1/user/999":
            return MockResponse(
                text_data="Not found.",
                json_data={},
                status_code=404,
                raise_for_status_flag=True,
                headers={},
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    # pylint: disable=no-method-argument
    def mocked_requests_delete(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/user/999":
            return MockResponse(
                text_data="Not found.",
                json_data={},
                status_code=404,
                raise_for_status_flag=True,
                headers={},
            )
        if args[0] == "https://127.0.0.1:8080/api/v1/user/123":
            return MockResponse(json_data={}, status_code=200, headers={},)
        raise RuntimeError("Unhandle GET request: " + args[0])

    def mocked_requests_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={
                    "location": (
                        "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                    )
                },
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    # delete() does a get() request to check the worker has 'purpose':'proxy'
    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.delete", side_effect=mocked_requests_delete)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_delete_user(self, mock_get, mock_post, mock_delete):
        with self.assertRaisesRegexp(
            AssertionError, "'id' must be provided and must be a str",
        ):
            get_client().user.delete(id=999)

        with self.assertRaisesRegexp(
            AssertionError, "'id' does not start with '/api/v1/user/'",
        ):
            get_client().user.delete(id="garbage")

        with self.assertRaises(APIItemNotFoundException):
            get_client().user.delete(id="/api/v1/user/999")

        get_client().user.delete(id="/api/v1/user/123")


def mocked_login_post(*args, **kwargs):
    if args[0] == "https://127.0.0.1:8080/api/v1/login":
        return MockResponse(
            json_data={},
            status_code=200,
            headers={
                "location": (
                    "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                )
            },
        )
    if args[0] == "https://127.0.0.1:8080/api/v1/user":
        return MockResponse(
            json_data={},
            status_code=200,
            headers={"location": ("/mock/api/user/1")},
        )
    raise RuntimeError("Unhandle POST request: " + args[0])


class TestCLI(BaseTestCase):
    @patch("requests.post", side_effect=mocked_login_post)
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
