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


import os
import sys
import unittest
from textwrap import dedent
import json
import yaml

import requests
from mock import patch

from hpecp import ContainerPlatformClient
from hpecp.exceptions import APIItemNotFoundException
import tempfile
from hpecp.base_resource import ResourceList

from .base_test import BaseTestCase, MockResponse, mocked_login_post
import six


class TestCLIList(BaseTestCase):
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/lock":
            return MockResponse(
                json_data={
                    "_links": {"self": {"href": "/api/v1/lock"}},
                    "locked": False,
                    "_embedded": {"internal_locks": [], "external_locks": []},
                },
                status_code=200,
                headers=dict(),
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.post", side_effect=mocked_login_post)
    @patch("requests.get", side_effect=mocked_requests_get)
    def test_list(self, mock_post, mock_get):

        try:
            hpecp = self.cli.CLI()
            hpecp.lock.list()
        except Exception as e:
            # Unexpected Exception
            self.fail(e)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = """\
_embedded:
  external_locks: []
  internal_locks: []
_links:
  self:
    href: /api/v1/lock
locked: false"""

        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)


class TestCLIDelete(BaseTestCase):
    def mocked_requests_delete(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/lock/1":
            return MockResponse(json_data={}, status_code=201, headers=dict(),)
        raise RuntimeError("Unhandle DELETE request: " + args[0])

    @patch("requests.post", side_effect=mocked_login_post)
    @patch("requests.delete", side_effect=mocked_requests_delete)
    def test_delete(self, mock_post, mock_delete):

        try:
            hpecp = self.cli.CLI()
            hpecp.lock.delete(id="/api/v1/lock/1")
        except Exception as e:
            # Unexpected Exception
            self.fail(e)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = ""
        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)


class TestCLICreate(BaseTestCase):
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
        elif args[0] == "https://127.0.0.1:8080/api/v1/lock":
            return MockResponse(
                json_data={},
                status_code=201,
                headers={"Location": "/test_location/1"},
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_post)
    def test_create(self, mock_post):

        try:
            hpecp = self.cli.CLI()
            hpecp.lock.create(reason="update")
        except Exception as e:
            # Unexpected Exception
            self.fail(e)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = "/test_location/1"
        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)

    def mocked_requests_post_with_exception(*args, **kwargs):
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
        elif args[0] == "https://127.0.0.1:8080/api/v1/lock":
            return MockResponse(
                json_data={},
                status_code=400,
                raise_for_status_flag=True,
                headers={},
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_post_with_exception)
    def test_create_with_exception(self, mock_post):

        with self.assertRaises(SystemExit) as cm:
            hpecp = self.cli.CLI()
            hpecp.lock.create(reason="update")

        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = ""
        expected_stderr = (
            "Unknown error. To debug run with env var LOG_LEVEL=DEBUG"
        )

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        self.assertTrue(
            stderr.endswith(expected_stderr),
            "expected: `{}` actual: `{}`".format(expected_stderr, stderr),
        )