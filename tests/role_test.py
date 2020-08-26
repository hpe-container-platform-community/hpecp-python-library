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
from unittest import TestCase

import six
from mock import patch

from .base import BaseTestCase, get_client
from .role_mock_api_responses import mockApiSetup

# setup the mock data
mockApiSetup()


class TestRoleGet(TestCase):
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_role_assertions(self, mock_get, mock_post):

        with self.assertRaisesRegexp(
            AssertionError,
            "'id' must be provided and must be a str",
        ):
            get_client().role.get(123)

        # pylint: disable=anomalous-backslash-in-string
        with self.assertRaisesRegexp(
            AssertionError,
            "'id' does not start with '/api/v1/role/",
        ):
            get_client().role.get("garbage")

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_role(self, mock_get, mock_post):

        role = get_client().role.get("/api/v1/role/1")

        self.assertEqual(role.id, "/api/v1/role/1")
        self.assertEqual(role.name, "Site Admin")
        self.assertEqual(role.description, "Role for Site Admin")


class TestCLI(BaseTestCase):
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get(self, mock_post, mock_delete):

        try:
            hpecp = self.cli.CLI()
            hpecp.role.get("/api/v1/role/1")
        except Exception as e:
            # Unexpected Exception
            self.fail(e)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = """\
_links:
  all_roles:
    href: /api/v1/role
  self:
    href: /api/v1/role/1
label:
  description: Role for Site Admin
  name: Site Admin"""

        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_json(self, mock_post, mock_delete):

        try:
            hpecp = self.cli.CLI()
            hpecp.role.get("/api/v1/role/1", output="json")
        except Exception as e:
            # Unexpected Exception
            self.fail(e)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        stdout = json.dumps(json.loads(stdout), sort_keys=True)

        expected_stdout = json.dumps(
            {
                "label": {
                    "description": "Role for Site Admin",
                    "name": "Site Admin",
                },
                "_links": {
                    "all_roles": {"href": "/api/v1/role"},
                    "self": {"href": "/api/v1/role/1"},
                },
            },
            sort_keys=True,
        )

        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)
