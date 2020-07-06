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

import requests
from mock import patch

from hpecp import ContainerPlatformClient
from hpecp.exceptions import APIItemNotFoundException
import tempfile
from hpecp.base_resource import ResourceList

from .base_test import BaseTestCase

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
        return MockResponse(
            json_data={
                "_links": {
                    "self": {"href": "/api/v1/catalog/99"},
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
                "id": "/api/v1/catalog/99",
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
            },
            status_code=200,
            headers=dict(),
        )
    if args[0] == "https://127.0.0.1:8080/api/v1/catalog/100":
        return MockResponse(
            json_data={
                "_links": {
                    "self": {"href": "/api/v1/catalog/100"},
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
                "id": "/api/v1/catalog/100",
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
            },
            status_code=200,
            headers=dict(),
        )
    if args[0] == "https://127.0.0.1:8080/api/v1/catalog/101":
        raise APIItemNotFoundException(
            message="catalog not found with id: " + "/api/v1/catalog/101",
            request_method="get",
            request_url=args[0],
        )
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
            AssertionError, "'id' must be provided and must be a str",
        ):
            get_client().catalog.get(123)

        with self.assertRaisesRegexp(
            AssertionError, "'id' must be provided and must be a str",
        ):
            get_client().catalog.get(False)

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_catalog_id_format(self, mock_get, mock_post):

        with self.assertRaisesRegexp(
            AssertionError, "'id' does not start with '/api/v1/catalog'"
        ):
            get_client().catalog.get("garbage")

    # @unittest.skip("This does not work yet!")
    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_catalog(self, mock_get, mock_post):

        catalog = get_client().catalog.get("/api/v1/catalog/99")

        self.assertEqual(catalog.id, "/api/v1/catalog/99")

        # TODO: test other property accessors
        with self.assertRaisesRegexp(
            APIItemNotFoundException,
            "'catalog not found with id: " + r"\/api\/v1\/catalog\/101",
        ):
            get_client().catalog.get("/api/v1/catalog/101")


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
    def mocked_requests_list(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/catalog":
            return MockResponse(
                json_data=catalog_list_json, status_code=200, headers=dict(),
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_list)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_list(self, mock_get, mock_post):

        catalog_list = get_client().catalog.list()
        self.assertIsInstance(catalog_list, ResourceList)


class TestCatalogInstall(unittest.TestCase):
    def mocked_requests_install(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/catalog/99":
            return MockResponse(json_data={}, status_code=204, headers=dict())
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return session_mock_response()
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_install)
    @patch("requests.get", side_effect=mocked_requests_get)
    def test_catalog_install(self, mock_get, mock_post):

        client = get_client()

        with self.assertRaisesRegexp(
            AssertionError, "'id' must be provided and must be a str",
        ):
            client.catalog.install(999)

        with self.assertRaisesRegexp(
            AssertionError, "'id' does not start with '/api/v1/catalog'",
        ):
            client.catalog.install("garbage")

        with self.assertRaisesRegexp(
            APIItemNotFoundException,
            "'catalog not found with id: /api/v1/catalog/101'",
        ):
            client.catalog.install("/api/v1/catalog/101")

        client.catalog.install("/api/v1/catalog/99")


class TestCatalogRefresh(unittest.TestCase):
    def mocked_requests_refresh(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/catalog/99":
            return MockResponse(json_data={}, status_code=204, headers=dict())
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return session_mock_response()
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_refresh)
    @patch("requests.get", side_effect=mocked_requests_get)
    def test_catalog_refresh(self, mock_get, mock_post):

        client = get_client()

        with self.assertRaisesRegexp(
            AssertionError, "'id' must be provided and must be a str",
        ):
            client.catalog.install(999)

        with self.assertRaisesRegexp(
            AssertionError, "'id' does not start with '/api/v1/catalog'",
        ):
            client.catalog.refresh("garbage")

        with self.assertRaisesRegexp(
            APIItemNotFoundException,
            "'catalog not found with id: /api/v1/catalog/101'",
        ):
            client.catalog.refresh("/api/v1/catalog/101")

        client.catalog.refresh("/api/v1/catalog/99")


class TestCLI(BaseTestCase):

    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/catalog":
            return MockResponse(
                json_data=catalog_list_json, status_code=200, headers=dict(),
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("requests.get", side_effect=mocked_requests_get)
    def test_cli_with_columns_and_table_output(self, mock_post, mock_get):

        self.maxDiff = None

        hpecp = self.cli.CLI()
        hpecp.catalog.list(columns=["label_name", "label_description"])

        output = self.out.getvalue().strip()
        
        self.assertEqual(
            output,
           "+------------+--------------------------------------------------------------------------------+\n"+
           "| label_name |                               label_description                                |\n"+
           "+------------+--------------------------------------------------------------------------------+\n"+
           "|  Spark240  | Spark240 multirole with Jupyter Notebook, Jupyterhub with SSL and gateway node |\n"+
           "+------------+--------------------------------------------------------------------------------+"
           )

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("requests.get", side_effect=mocked_requests_get)
    def test_cli_with_columns_and_text_output(self, mock_post, mock_get):

        self.maxDiff = None

        hpecp = self.cli.CLI()
        hpecp.catalog.list(columns=["label_name", "distro_id"], output="text")

        output = self.out.getvalue().strip()        
        self.assertEqual(
            output,
           "Spark240  bluedata/spark240juphub7xssl"
           )


    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("requests.get", side_effect=mocked_requests_get)
    def test_cli_with_query(self, mock_post, mock_get):

        self.maxDiff = None

        hpecp = self.cli.CLI()
        hpecp.catalog.list(query="[*][_links.self.href, distro_id]", output="json")

        output = self.out.getvalue().strip()

        try:
            json.loads(output)
        except Exception:
            self.fail("Output should be valid json")
        
        self.assertEqual(
            output,
            '[["/api/v1/catalog/29", "bluedata/spark240juphub7xssl"]]'
            )
