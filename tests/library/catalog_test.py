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

import requests
from mock import patch

from hpecp import ContainerPlatformClient
from hpecp.catalog import CatalogList
from hpecp.exceptions import APIItemNotFoundException
import tempfile


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


def session_mock_response():
    return MockResponse(
        json_data={},
        status_code=200,
        headers={
            "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
        },
    )


def mocked_requests_get(*args, **kwargs):
    if args[0] == "https://127.0.0.1:8080/api/v1/catalog/99":
        return MockResponse(json_data=dict(), status_code=200, headers=dict())
    if args[0] == "https://127.0.0.1:8080/api/v1/catalog/100":
        return MockResponse(json_data=dict(), status_code=200, headers=dict())
    raise RuntimeError("Unhandle GET request: " + args[0])


def mocked_requests_post(*args, **kwargs):
    if args[0] == "https://127.0.0.1:8080/api/v1/login":
        return session_mock_response()
    raise RuntimeError("Unhandle POST request: " + args[0])


class TestCatalogGet(unittest.TestCase):
    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_catalog_id_type(self, mock_get, mock_post):

        with self.assertRaisesRegexp(
            AssertionError,
            "'catalog_id' must be provided and must be a string",
        ):
            get_client().catalog.get(123)

        with self.assertRaisesRegexp(
            AssertionError,
            "'catalog_id' must be provided and must be a string",
        ):
            get_client().catalog.get(False)

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_catalog_id_format(self, mock_get, mock_post):

        with self.assertRaisesRegexp(
            AssertionError,
            "'catalog_id' must have format "
            + r"'\/api\/v1\/catalog\/\[0-9\]\+'",
        ):
            get_client().catalog.get("garbage")

        with self.assertRaisesRegexp(
            AssertionError,
            "'catalog_id' must have format "
            + r"'\/api\/v1\/catalog\/\[0-9\]\+'",
        ):
            get_client().catalog.get("/api/v1/catalog/some_id")

    @unittest.skip("This does not work yet!")
    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_catalog(self, mock_get, mock_post):

        catalog = get_client().catalog.get("/api/v1/catalog/99")

        self.assertEqual(catalog.id, "/api/v1/catalog/99")

        # TODO: test other property accessors
        with self.assertRaisesRegexp(
            APIItemNotFoundException,
            "'catalog not found with id: /api/v1/catalog/100'",
        ):
            get_client().catalog.get("/api/v1/catalog/100")


catalog_list_json = {
    "_links": {
        "self": {"href": "/api/v1/catalog/"},
        "feedlog": {"href": "/api/v1/catalog/feedlog"},
        "feed": [
            {
                "href": "http://127.0.0.1:8080/api/v1/feed/local",
                "name": "Feed generated from local bundles.",
            },
            {
                "href": (
                    "https://s3.amazonaws.com/bluedata-catalog/bundles/"
                    "catalog/external/docker/EPIC-5.0/feeds/feed.json"
                ),
                "name": "BlueData EPIC-5.0 catalog feed for docker",
            },
        ],
    },
    "catalog_api_version": 6,
    "feeds_refresh_period_seconds": 86400,
    "feeds_read_counter": 5,
    "catalog_write_counter": 5,
    "_embedded": {
        "independent_catalog_entries": [
            {
                "_links": {
                    "self": {"href": "/api/v1/catalog/29"},
                    "feed": [
                        {
                            "href": (
                                "https://s3.amazonaws.com/bluedata-catalog/"
                                "bundles/catalog/external/docker/EPIC-5.0/"
                                "feeds/feed.json"
                            ),
                            "name": (
                                "BlueData EPIC-5.0 catalog feed for docker"
                            ),
                        }
                    ],
                },
                "distro_id": "bluedata/spark240juphub7xssl",
                "label": {
                    "name": "Spark240",
                    "description": (
                        "Spark240 multirole with Jupyter Notebook, Jupyterhub"
                        " with SSL and gateway node"
                    ),
                },
                "version": "2.8",
                "timestamp": 0,
                "isdebug": False,
                "osclass": ["centos"],
                "logo": {
                    "checksum": "1471eb59356066ed4a06130566764ea6",
                    "url": (
                        "http://10.1.0.53/catalog/logos/"
                        "bluedata-spark240juphub7xssl-2.8"
                    ),
                },
                "documentation": {
                    "checksum": "52f53f1b2845463b9e370d17fb80bea6",
                    "mimetype": "text/markdown",
                    "file": (
                        "/opt/bluedata/catalog/documentation/"
                        "bluedata-spark240juphub7xssl-2.8"
                    ),
                },
                "state": "initialized",
                "state_info": "",
            }
        ]
    },
}


class TestCatalogList(unittest.TestCase):
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/catalog/":
            return MockResponse(
                json_data=catalog_list_json, status_code=200, headers=dict(),
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_list(self, mock_get, mock_post):

        catalogList = get_client().catalog.list()
        self.assertIsInstance(catalogList, CatalogList)


class TestCLI(unittest.TestCase):
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

        sys.path.insert(0, os.path.abspath("../../"))
        from bin import cli

        self.cli = cli
        self.cli.HPECP_CONFIG_FILE = self.tmpFile.name

    def tearDown(self):
        self.tmpFile.close()

    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/catalog/":
            return MockResponse(
                json_data=catalog_list_json, status_code=200, headers=dict(),
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("requests.get", side_effect=mocked_requests_get)
    def test_cli(self, mock_post, mock_get):

        hpecp = self.cli.CLI()
        hpecp.catalog.list()

        self.assertTrue(True)
