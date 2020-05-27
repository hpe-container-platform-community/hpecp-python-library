import unittest

import requests
from mock import patch

from hpecp import ContainerPlatformClient
from hpecp.exceptions import APIItemNotFoundException


class MockResponse:
    def __init__(
        self, json_data, status_code, headers, raise_for_status_flag=False, text_data=""
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
        headers={"location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"},
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
            AssertionError, "'catalog_id' must be provided and must be a string"
        ):
            get_client().catalog.get(123)

        with self.assertRaisesRegexp(
            AssertionError, "'catalog_id' must be provided and must be a string"
        ):
            get_client().catalog.get(False)

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_catalog_id_format(self, mock_get, mock_post):

        with self.assertRaisesRegexp(
            AssertionError,
            "'catalog_id' must have format " + r"'\/api\/v1\/catalog\/\[0-9\]\+'",
        ):
            get_client().catalog.get("garbage")

        with self.assertRaisesRegexp(
            AssertionError,
            "'catalog_id' must have format " + r"'\/api\/v1\/catalog\/\[0-9\]\+'",
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
            APIItemNotFoundException, "'catalog not found with id: /api/v1/catalog/100'"
        ):
            get_client().catalog.get("/api/v1/catalog/100")
