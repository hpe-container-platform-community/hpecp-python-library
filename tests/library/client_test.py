from unittest import TestCase
from mock import Mock, patch, mock_open

from textwrap import dedent
import sys
import tempfile
import os
import json
import requests
from requests.exceptions import RequestException
from hpecp import ContainerPlatformClient


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


class TestCreateFromProperties(TestCase):
    def test_create_from_config_file_factory_method(self):
        file_data = dedent(
            """[default]
                              api_host = 127.0.0.1
                              api_port = 8080
                              use_ssl = True
                              verify_ssl = False
                              warn_ssl = True
                              username = admin
                              password = admin123"""
        )

        tmp = tempfile.NamedTemporaryFile(delete=True)
        try:
            tmp.write(file_data.encode("utf-8"))
            tmp.flush()

            client = ContainerPlatformClient.create_from_config_file(
                config_file=tmp.name
            )
            self.assertEqual(client.username, "admin")
            self.assertEqual(client.password, "admin123")
            self.assertEqual(client.api_host, "127.0.0.1")
            self.assertEqual(client.api_port, 8080)
            self.assertEqual(client.use_ssl, True)
            self.assertEqual(client.verify_ssl, False)
            self.assertEqual(client.warn_ssl, True)
        finally:
            tmp.close()


class TestAuth(TestCase):

    # pylint: disable=no-method-argument
    def mocked_requests_post(*args, **kwargs):
        if args[0] == "http://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={
                    "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                },
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_post)
    def test_create_session(self, mock_post):

        client = ContainerPlatformClient(
            username="admin",
            password="admin123",
            api_host="127.0.0.1",
            api_port=8080,
            use_ssl=False,
        )

        self.assertIsInstance(client.create_session(), ContainerPlatformClient)

    @patch("requests.post", side_effect=mocked_requests_post)
    def test_create_session_chained(self, mock_post):

        client = ContainerPlatformClient(
            username="admin",
            password="admin123",
            api_host="127.0.0.1",
            api_port=8080,
            use_ssl=False,
        ).create_session()

        self.assertIsInstance(client, ContainerPlatformClient)

    def mocked_requests_post_ssl(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={
                    "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                },
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_post_ssl)
    def test_auth_ssl(self, mock_post):

        client = ContainerPlatformClient(
            username="admin",
            password="admin123",
            api_host="127.0.0.1",
            api_port=8080,
            use_ssl=True,
        )
        client.create_session()

    def mocked_requests_post_return_500(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=500,
                headers={},
                raise_for_status_flag=True,
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_post_return_500)
    def test_auth_ssl_with_error(self, mock_post):

        client = ContainerPlatformClient(
            username="admin",
            password="admin123",
            api_host="127.0.0.1",
            api_port=8080,
            use_ssl=True,
        )

        with self.assertRaises(requests.exceptions.HTTPError):
            client.create_session()
