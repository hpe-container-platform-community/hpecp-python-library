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

import abc
import os
import sys
import tempfile
from io import StringIO
from textwrap import dedent
from unittest import TestCase
import json
import unittest
import requests
import six
from mock import patch

from hpecp import (
    APIException,
    APIItemNotFoundException,
    ContainerPlatformClient,
)
from hpecp.k8s_cluster import (
    K8sCluster,
    K8sClusterHostConfig,
    K8sClusterStatus,
)

if six.PY2:
    from io import BytesIO as StringIO  # noqa: F811
else:
    from io import StringIO


def session_mock_response():
    return MockResponse(
        json_data={},
        status_code=200,
        headers={
            "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
        },
    )


class MockResponse:
    def __init__(
        self,
        json_data,
        status_code,
        headers,
        raise_for_status_flag=False,
        raise_connection_error=False,
        text_data="",
    ):
        self.json_data = json_data
        self.text = text_data
        self.status_code = status_code
        self.raise_for_status_flag = raise_for_status_flag
        self.raise_connection_error = raise_connection_error
        self.headers = headers

    def raise_for_status(self):
        if self.raise_for_status_flag:
            self.text = "some error occurred"
            raise requests.exceptions.HTTPError()
        if self.raise_connection_error:
            self.text = "Simulating a connection error"
            raise requests.exceptions.ConnectionError()
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


# pylint: disable=no-method-argument
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
    raise RuntimeError("Unhandle POST request: " + args[0])


@six.add_metaclass(abc.ABCMeta)
class BaseTestCase(unittest.TestCase):
    def setUp(self):
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

        self.tmpFile = tempfile.NamedTemporaryFile(delete=True)
        self.tmpFile.write(file_data.encode("utf-8"))
        self.tmpFile.flush()

        self.saved_stdout = sys.stdout
        self.out = StringIO()
        sys.stdout = self.out

        self.saved_stderr = sys.stderr
        self.err = StringIO()
        sys.stderr = self.err

        sys.path.insert(0, os.path.abspath("../../"))
        from bin import cli

        self.cli = cli
        self.cli.HPECP_CONFIG_FILE = self.tmpFile.name

    def tearDown(self):
        self.tmpFile.close()
        sys.stdout = self.saved_stdout
        sys.stderr = self.saved_stderr
