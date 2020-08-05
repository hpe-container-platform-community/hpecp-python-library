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

from .base import BaseTestCase
from .license_mock_api_responses import mockApiSetup

# setup the mock data
mockApiSetup()


class TestCLI(BaseTestCase):
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_list(self, mock_post, mock_get):

        try:
            hpecp = self.cli.CLI()
            hpecp.license.list()
        except Exception as e:
            # Unexpected Exception
            self.fail(e)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = """\
Enabled: true
Licenses:
- Capacity: 240
  DeviceID: 1234 1234
  Evaluation: false
  Expiration: 1609286399000
  ExpirationDisplay: \'2020-12-29T23:59:59Z\'
  Feature: HPE Machine Learning Ops
  Label: The License
  LicenseKey: TEST_LICENSE_KEY
  Start: 1566864000000
  StartDisplay: \'2019-08-27T00:00:00Z\'
  UnlimitedCapacity: false
Messages: []
RevalidateTime: 1609286400000
Summaries:
- AvailableCapacity: 216
  Label: HPE Container Platform
  LatestExpiration: 1609286399000
  LatestExpirationDisplay: \'2020-12-29T23:59:59Z\'
  NextExpiration: 1609286399000
  NextExpirationDisplay: \'2020-12-29T23:59:59Z\'
  RevalidateTime: 1609286400000
  TotalCapacity: 240
  UnlimitedCapacity: false
  UsedCapacity: 24
  Valid: true
  ValidationTime: 1594758782000
- AvailableCapacity: 240
  Label: HPE Machine Learning Ops
  LatestExpiration: 1609286399000
  LatestExpirationDisplay: \'2020-12-29T23:59:59Z\'
  NextExpiration: 1609286399000
  NextExpirationDisplay: \'2020-12-29T23:59:59Z\'
  RevalidateTime: 1609286400000
  TotalCapacity: 240
  UnlimitedCapacity: false
  UsedCapacity: 0
  Valid: true
  ValidationTime: 1594758782000
Valid: true
ValidationTime: 1594758782000
_links:
  self:
    href: /api/v2/hpelicense"""

        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_list_license_key_only(self, mock_post, mock_get):

        try:
            hpecp = self.cli.CLI()
            hpecp.license.list(license_key_only=True)
        except Exception as e:
            # Unexpected Exception
            self.fail(e)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = "TEST_LICENSE_KEY"
        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_list_output_json(self, mock_post, mock_get):

        self.maxDiff = None

        try:
            hpecp = self.cli.CLI()
            hpecp.license.list(output="json")
        except Exception as e:
            # Unexpected Exception
            self.fail(e)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        stdout = json.dumps(json.loads(stdout), sort_keys=True)
        expected_stdout = json.dumps(
            {
                "_links": {"self": {"href": "/api/v2/hpelicense"}},
                "RevalidateTime": 1609286400000,
                "ValidationTime": 1594758782000,
                "Valid": True,
                "Licenses": [
                    {
                        "Expiration": 1609286399000,
                        "DeviceID": "1234 1234",
                        "Evaluation": False,
                        "Capacity": 240,
                        "UnlimitedCapacity": False,
                        "StartDisplay": "2019-08-27T00:00:00Z",
                        "Start": 1566864000000,
                        "LicenseKey": "TEST_LICENSE_KEY",
                        "ExpirationDisplay": "2020-12-29T23:59:59Z",
                        "Feature": "HPE Machine Learning Ops",
                        "Label": "The License",
                    }
                ],
                "Messages": [],
                "Enabled": True,
                "Summaries": [
                    {
                        "NextExpiration": 1609286399000,
                        "LatestExpirationDisplay": "2020-12-29T23:59:59Z",
                        "TotalCapacity": 240,
                        "Valid": True,
                        "UnlimitedCapacity": False,
                        "UsedCapacity": 24,
                        "RevalidateTime": 1609286400000,
                        "ValidationTime": 1594758782000,
                        "AvailableCapacity": 216,
                        "Label": "HPE Container Platform",
                        "NextExpirationDisplay": "2020-12-29T23:59:59Z",
                        "LatestExpiration": 1609286399000,
                    },
                    {
                        "NextExpiration": 1609286399000,
                        "LatestExpirationDisplay": "2020-12-29T23:59:59Z",
                        "TotalCapacity": 240,
                        "Valid": True,
                        "UnlimitedCapacity": False,
                        "UsedCapacity": 0,
                        "RevalidateTime": 1609286400000,
                        "ValidationTime": 1594758782000,
                        "AvailableCapacity": 240,
                        "Label": "HPE Machine Learning Ops",
                        "NextExpirationDisplay": "2020-12-29T23:59:59Z",
                        "LatestExpiration": 1609286399000,
                    },
                ],
            },
            sort_keys=True,
        )
        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_platform_id(self, mock_post, mock_get):

        try:
            hpecp = self.cli.CLI()
            hpecp.license.platform_id()
        except Exception as e:
            # Unexpected Exception
            self.fail(e)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = """3c831f6e-f76f-410d-977c-ed13b0c817d1"""
        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_register(self, mock_post, mock_get):

        try:
            hpecp = self.cli.CLI()
            hpecp.license.register(server_filename="abc")
        except Exception as e:
            # Unexpected Exception
            self.fail(e)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = "/api/v2/hpeclicense/1"
        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.delete", side_effect=BaseTestCase.httpDeleteHandlers)
    def test_delete(self, mock_post, mock_delete):

        with patch.dict("os.environ", {"LOG_LEVEL": "DEBUG"}):
            hpecp = self.cli.CLI()
            hpecp.license.delete(license_key="TEST_LICENSE_KEY")

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = ""
        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.delete", side_effect=BaseTestCase.httpDeleteHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_delete_all(self, mock_post, mock_delete, mock_get):

        with patch.dict("os.environ", {"LOG_LEVEL": "DEBUG"}):
            hpecp = self.cli.CLI()
            hpecp.license.delete_all()

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = ""
        expected_stderr = ""

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error on PY3 (issues 93)
        if six.PY2:
            self.assertEqual(stderr, expected_stderr)
