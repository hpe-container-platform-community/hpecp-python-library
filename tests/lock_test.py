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


import json

import six
from mock import patch

from .base import BaseTestCase, MockResponse
from .lock_mock_api_responses import mockApiSetup

# setup the mock data
mockApiSetup()


class TestCLIList(BaseTestCase):
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_list_yaml(self, mock_post, mock_get):

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

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_list_json(self, mock_post, mock_get):

        self.maxDiff = None

        try:
            hpecp = self.cli.CLI()
            hpecp.lock.list(output="json")
        except Exception as e:
            # Unexpected Exception
            self.fail(e)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = json.dumps(
            {
                "_links": {"self": {"href": "/api/v1/lock"}},
                "locked": False,
                "_embedded": {"internal_locks": [], "external_locks": []},
            }
        )
        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            expected_stderr = ""
            self.assertEqual(stderr, expected_stderr)

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_list_output_parameter_invalid(self, mock_post, mock_get):

        self.maxDiff = None

        with self.assertRaises(SystemExit) as cm:
            hpecp = self.cli.CLI()
            hpecp.lock.list(output="garbage")

        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = ""
        self.assertEqual(stdout, expected_stdout)

        expected_stderr = "'output' parameter must be 'yaml' or 'json'"
        self.assertEqual(stderr, expected_stderr)


class TestCLIDelete(BaseTestCase):
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.delete", side_effect=BaseTestCase.httpDeleteHandlers)
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

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.delete", side_effect=BaseTestCase.httpDeleteHandlers)
    def test_delete_all(self, mock_get, mock_post, mock_delete):

        try:
            hpecp = self.cli.CLI()
            hpecp.lock.delete_all()
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

    def mocked_requests_get_locked(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/lock":
            return MockResponse(
                json_data={
                    "_links": {"self": {"href": "/api/v1/lock"}},
                    "locked": True,
                    "_embedded": {
                        "internal_locks": ["1"],
                        "external_locks": [],
                    },
                },
                status_code=200,
                headers=dict(),
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_get_locked)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.delete", side_effect=BaseTestCase.httpDeleteHandlers)
    def test_delete_all_timeout(self, mock_get, mock_post, mock_delete):

        with self.assertRaises(SystemExit) as cm:
            hpecp = self.cli.CLI()
            hpecp.lock.delete_all(timeout_secs=1)

        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = ""
        expected_stderr = "Could not delete locks."

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)


class TestCLICreate(BaseTestCase):
    def mocked_requests_get_locked(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/lock":
            return MockResponse(
                json_data={
                    "_links": {"self": {"href": "/api/v1/lock"}},
                    "locked": True,
                    "quiesced": True,
                    "_embedded": {
                        "internal_locks": ["1"],
                        "external_locks": [],
                    },
                },
                status_code=200,
                headers=dict(),
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=mocked_requests_get_locked)
    def test_create(self, mock_post, mock_get):

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

        self.assertEqual(
            stdout,
            expected_stdout,
            "Expected: '{}' Actual: '{}'".format(expected_stdout, stdout),
        )

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
