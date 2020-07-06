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
import tempfile
from textwrap import dedent
from unittest import TestCase

import requests
import six
from mock import mock, mock_open, patch

from .base_test import BaseTestCase

if six.PY2:
    from io import BytesIO as StringIO  # noqa: F811
    from test.test_support import EnvironmentVarGuard
else:
    from io import StringIO
    from test.support import EnvironmentVarGuard

try:
    from imp import reload
except Exception:
    from importlib import reload


class TestCLI(BaseTestCase):
    def test_config_file_missing(self):

        with self.assertRaises(SystemExit) as cm:
            self.cli.HPECP_CONFIG_FILE = "this_file_should_not_exist"
            self.cli.get_client()

        self.assertEqual(cm.exception.code, 1)

        self.assertEqual(self.out.getvalue(), "")

        self.assertEqual(
            self.err.getvalue(),
            "Could not find configuration file 'this_file_should_not_exist'\n",
        )

    def test_configure_cli_writes_hpecp_conf(self):

        if six.PY2:
            builtins_name = "__builtin__.open"
        else:
            builtins_name = "builtins.open"

        with patch(builtins_name, mock_open()) as m:

            # mock the input capture to simulate user input
            # TODO: we want to send different data for each parameter
            six.moves.input = lambda *args: ("1234")

            hpecp = self.cli.CLI()
            hpecp.configure_cli()

        handle = m()
        handle.write.assert_has_calls(
            [
                mock.call("[default]\n"),
                mock.call("api_host = 1234\n"),
                mock.call("api_port = 1234\n"),
                mock.call("use_ssl = 1234\n"),
                mock.call("verify_ssl = 1234\n"),
                mock.call("warn_ssl = 1234\n"),
                mock.call("username = 1234\n"),
                mock.call("password = 1234\n"),
                mock.call("\n"),
            ]
        )

    def test_configure_cli_reads_hpecp_conf(self):

        mock_data = dedent(
            """                [default]
                api_host = mock_host
                api_port = 9999
                use_ssl = True
                verify_ssl = False
                warn_ssl = True
                username = admin
                password = admin123"""
        ).encode("utf8")

        if six.PY2:
            builtins_name = "__builtin__.open"
        else:
            builtins_name = "builtins.open"

        with patch(builtins_name, mock_open(read_data=mock_data)):
            with patch("os.path.exists") as os_path_exists:

                # instruct the CLI that the mock file is actually
                # ~/.hpecp.conf
                os_path_exists.return_value = True

                # mock the input capture to simulate user input
                # TODO: we want to send different data for each configuration
                # parameter
                six.moves.input = lambda *args: ("1234")

                hpecp = self.cli.CLI()
                hpecp.configure_cli()

                self.assertIn(
                    "Controller API Host [mock_host]:", self.out.getvalue()
                )
                self.assertIn(
                    "Controller API Port [9999]:", self.out.getvalue()
                )
                # TODO check all values

    def test_autocomplete_bash(self):

        try:
            hpecp = self.cli.CLI()
            hpecp.autocomplete.bash()
        except Exception:
            self.fail("Unexpected exception.")


class TestCLIUsingCfgFileEnvVar(TestCase):
    def test_hpe_config_file_var(self):
        dummy_filepath = "/not/a/real/dir/not_a_real_file"

        env = EnvironmentVarGuard()
        env.set("HPECP_CONFIG_FILE", dummy_filepath)

        with env:
            sys.path.insert(0, os.path.abspath("../../"))
            from bin import cli

            # reload cli module with mock env
            reload(cli)

            self.assertEqual(dummy_filepath, cli.HPECP_CONFIG_FILE)


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


def session_mock_response():
    return MockResponse(
        json_data={},
        status_code=200,
        headers={
            "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
        },
    )


class TestCLIHttpClient(BaseTestCase):
    def mocked_requests_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return session_mock_response()
        raise RuntimeError("Unhandle POST request: " + args[0])

    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/some/url":
            return MockResponse(
                json_data={"foo": "bar"},
                text_data='{"foo":"bar"}',
                status_code=200,
                headers=dict(),
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    def mocked_requests_failed_login(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={"foo": "bar"},
                text_data='{"foo":"bar"}',
                raise_connection_error=True,
                status_code=500,
                headers=dict(),
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_failed_login)
    def test_get_failed_login(self, mock_get, mock_post):

        # TODO move this to TestCLI class

        with self.assertRaises(SystemExit) as cm:
            hpecp = self.cli.CLI()
            hpecp.httpclient.get("/")  # our mock raises an exception on login

        self.assertEqual(cm.exception.code, 1)

        self.assertEqual(self.out.getvalue(), "")

        self.assertEqual(
            self.err.getvalue(),
            "Could not connect to controller - set LOG_LEVEL=DEBUG to see more detail.\n",
        )

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get(self, mock_get, mock_post):

        hpecp = self.cli.CLI()
        hpecp.httpclient.get(url="/some/url")

        self.assertEqual(self.out.getvalue(), '{"foo":"bar"}\n')

    def mocked_requests_delete(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/some/url":
            return MockResponse(
                json_data={"foo": "bar"},
                text_data='{"foo":"bar"}',
                status_code=200,
                headers=dict(),
            )
        raise RuntimeError("Unhandle DELETE request: " + args[0])

    @patch("requests.delete", side_effect=mocked_requests_delete)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_delete(self, mock_delete, mock_post):

        hpecp = self.cli.CLI()
        hpecp.httpclient.delete(url="/some/url")

        self.assertEqual(self.out.getvalue(), '{"foo":"bar"}\n')

    # TODO - add tests for POST and PUT
