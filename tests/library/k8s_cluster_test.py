from unittest import TestCase
from mock import Mock, patch

import sys
import tempfile
import os
import json
import requests
from requests.exceptions import RequestException
from hpecp import ContainerPlatformClient, APIException, APIItemNotFoundException
from hpecp.k8s_cluster import K8sClusterHostConfig, K8sClusterStatus


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


class TestClusterList(TestCase):

    # pylint: disable=no-method-argument
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v2/k8scluster":
            return MockResponse(
                json_data={
                    "_links": {"self": {"href": "/api/v2/k8scluster"}},
                    "_embedded": {
                        "k8sclusters": [
                            {
                                "_links": {"self": {"href": "/api/v2/k8scluster/20"}},
                                "label": {"name": "def", "description": "my cluster"},
                                "k8s_version": "1.17.0",
                                "pod_network_range": "10.192.0.0/12",
                                "service_network_range": "10.96.0.0/12",
                                "pod_dns_domain": "cluster.local",
                                "created_by_user_id": "/api/v1/user/5",
                                "created_by_user_name": "admin",
                                "created_time": 1588260014,
                                "k8shosts_config": [
                                    {
                                        "node": "/api/v2/worker/k8shost/4",
                                        "role": "worker",
                                    },
                                    {
                                        "node": "/api/v2/worker/k8shost/5",
                                        "role": "master",
                                    },
                                ],
                                "status": "ready",
                                "status_message": "really ready",
                                "api_endpoint_access": "api:1234",
                                "dashboard_endpoint_access": "dashboard:1234",
                                "admin_kube_config": "xyz==",
                                "dashboard_token": "abc==",
                                "persistent_storage": {"nimble_csi": False},
                            }
                        ]
                    },
                },
                status_code=200,
                headers={},
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    def mocked_requests_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={
                    "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                },
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_k8sclusters(self, mock_get, mock_post):

        # Makes GET Request: https://127.0.0.1:8080/api/v2/k8sclusters/
        clusters = get_client().k8s_cluster.list()

        # Test that json response is saved in each WorkerK8s object
        # assert client.k8s_cluster.get()[0].json is not None

        # Test WorkerK8sList subscriptable access and property setters
        self.assertEqual(clusters[0].id, "/api/v2/k8scluster/20")
        self.assertEqual(clusters[0].name, "def")
        self.assertEqual(clusters[0].description, "my cluster")
        self.assertEqual(clusters[0].k8s_version, "1.17.0")
        self.assertEqual(clusters[0].created_by_user_id, "/api/v1/user/5")
        self.assertEqual(clusters[0].created_by_user_name, "admin")
        self.assertEqual(clusters[0].created_time, 1588260014)

        self.maxDiff = None
        self.assertListEqual(
            clusters[0].k8shosts_config,
            [
                {"node": "/api/v2/worker/k8shost/4", "role": "worker"},
                {"node": "/api/v2/worker/k8shost/5", "role": "master"},
            ],
        )
        self.assertEqual(clusters[0].admin_kube_config, "xyz==")
        self.assertEqual(clusters[0].dashboard_token, "abc==")
        self.assertEqual(clusters[0].api_endpoint_access, "api:1234")
        self.assertEqual(clusters[0].dashboard_endpoint_access, "dashboard:1234")
        self.assertIsNone(
            clusters[0].cert_data
        )  # The cluster wasn't created with certs - TODO: need a test with this value set
        self.assertEqual(clusters[0].status, "ready")
        self.assertEqual(clusters[0].status_message, "really ready")
        self.assertDictEqual(
            clusters[0]._links, {"self": {"href": "/api/v2/k8scluster/20"}}
        )

        # Test iterators
        assert [cluster.id for cluster in get_client().k8s_cluster.list()] == [
            "/api/v2/k8scluster/20"
        ]

        with self.assertRaisesRegexp(
            AssertionError, "'columns' parameter must be list"
        ):
            get_client().k8s_cluster.list().tabulate(columns="garbage")

        # FIXME: This test doesn't work on 2.x or 3.5 - maybe just a string comparision issue?
        if sys.version_info[0] == 3 and sys.version_info[1] >= 6:
            self.maxDiff = None
            self.assertEqual(
                get_client().k8s_cluster.list().tabulate(),
                "+-----------------------+------+-------------+-------------+--------------------+----------------------+--------------+------------------------------------------------------------------------------------------------------------------+-------------------+-----------------+---------------------+---------------------------+-----------+--------+----------------+---------------------------------------------+\n"
                + "|          id           | name | description | k8s_version | created_by_user_id | created_by_user_name | created_time |                                                 k8shosts_config                                                  | admin_kube_config | dashboard_token | api_endpoint_access | dashboard_endpoint_access | cert_data | status | status_message |                   _links                    |\n"
                + "+-----------------------+------+-------------+-------------+--------------------+----------------------+--------------+------------------------------------------------------------------------------------------------------------------+-------------------+-----------------+---------------------+---------------------------+-----------+--------+----------------+---------------------------------------------+\n"
                + "| /api/v2/k8scluster/20 | def  | my cluster  |   1.17.0    |   /api/v1/user/5   |        admin         |  1588260014  | [{'node': '/api/v2/worker/k8shost/4', 'role': 'worker'}, {'node': '/api/v2/worker/k8shost/5', 'role': 'master'}] |       xyz==       |      abc==      |      api:1234       |      dashboard:1234       |           | ready  |  really ready  | {'self': {'href': '/api/v2/k8scluster/20'}} |\n"
                + "+-----------------------+------+-------------+-------------+--------------------+----------------------+--------------+------------------------------------------------------------------------------------------------------------------+-------------------+-----------------+---------------------+---------------------------+-----------+--------+----------------+---------------------------------------------+",
            )

        self.assertEqual(
            get_client().k8s_cluster.list().tabulate(["description", "id"]),
            "+-------------+-----------------------+\n"
            + "| description |          id           |\n"
            + "+-------------+-----------------------+\n"
            + "| my cluster  | /api/v2/k8scluster/20 |\n"
            + "+-------------+-----------------------+",
        )


class TestCreateCluster(TestCase):

    # pylint: disable=no-method-argument
    def mocked_requests_create_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={
                    "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                },
            )
        elif args[0] == "https://127.0.0.1:8080/api/v2/k8scluster":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={"Location": "/api/v2/k8sclusters/99"},
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_create_post)
    def test_create(self, mock_post):

        with self.assertRaisesRegexp(
            AssertionError, "'name' must be provided and must be a string"
        ):
            get_client().k8s_cluster.create()

        with self.assertRaisesRegexp(
            AssertionError, "'description' if provided, must be a string"
        ):
            get_client().k8s_cluster.create(name="a", description=1)

        with self.assertRaisesRegexp(
            AssertionError, "'k8s_version' if provided, must be a string"
        ):
            get_client().k8s_cluster.create(name="a", k8s_version=1)

        with self.assertRaisesRegexp(
            AssertionError, "'pod_network_range' must be a string"
        ):
            get_client().k8s_cluster.create(name="a", pod_network_range=1)

        with self.assertRaisesRegexp(
            AssertionError, "'service_network_range' must be a string"
        ):
            get_client().k8s_cluster.create(name="a", service_network_range=1)

        with self.assertRaisesRegexp(
            AssertionError, "'pod_dns_domain' must be a string"
        ):
            get_client().k8s_cluster.create(name="a", pod_dns_domain=1)

        with self.assertRaisesRegexp(
            AssertionError, "'persistent_storage_local' must be True or False"
        ):
            get_client().k8s_cluster.create(name="a", persistent_storage_local=1)

        with self.assertRaisesRegexp(
            AssertionError, "'persistent_storage_nimble_csi' must be True or False"
        ):
            get_client().k8s_cluster.create(name="a", persistent_storage_nimble_csi=1)

        with self.assertRaisesRegexp(
            AssertionError, "'k8shosts_config' must be a list"
        ):
            get_client().k8s_cluster.create(name="a", k8shosts_config=1)

        with self.assertRaisesRegexp(
            AssertionError, "'k8shosts_config' must have at least one item"
        ):
            get_client().k8s_cluster.create(name="a", k8shosts_config=[])

        with self.assertRaisesRegexp(
            AssertionError,
            "'k8shosts_config' item '0' is not of type K8sClusterHostConfig",
        ):
            get_client().k8s_cluster.create(name="a", k8shosts_config=[1, 2])

        # pylint: disable=anomalous-backslash-in-string
        with self.assertRaisesRegexp(
            AssertionError,
            "'node' must have format '\/api\/v2\/worker\/k8shost\/\[0-9\]\+'",
        ):
            get_client().k8s_cluster.create(
                name="a", k8shosts_config=[K8sClusterHostConfig("a", "b")]
            )

        with self.assertRaisesRegexp(
            AssertionError, "'role' must one of \['master, worker'\]"
        ):
            get_client().k8s_cluster.create(
                name="a",
                k8shosts_config=[K8sClusterHostConfig("/api/v2/worker/k8shost/1", "b")],
            )

        # Finally we can create a cluster
        id = get_client().k8s_cluster.create(
            name="a",
            k8shosts_config=[
                K8sClusterHostConfig("/api/v2/worker/k8shost/1", "master")
            ],
        )
        self.assertEqual(id, "/api/v2/k8sclusters/99")

    def mocked_requests_create_error_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={
                    "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                },
            )
        elif args[0] == "https://127.0.0.1:8080/api/v2/k8scluster":
            return MockResponse(
                json_data={}, raise_for_status_flag=True, status_code=500, headers={}
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_create_error_post)
    def test_create_with_APIException(self, mock_post):

        with self.assertRaises(APIException):
            get_client().k8s_cluster.create(
                name="a",
                k8shosts_config=[
                    K8sClusterHostConfig("/api/v2/worker/k8shost/1", "master")
                ],
            )


class TestGetCluster(TestCase):

    # pylint: disable=no-method-argument
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v2/k8scluster/999":
            return MockResponse(
                json_data={}, status_code=404, raise_for_status_flag=True, headers={}
            )
        if args[0] == "https://127.0.0.1:8080/api/v2/k8scluster/123":
            return MockResponse(
                json_data={
                    "_links": {"self": {"href": "/api/v2/k8scluster/123"}},
                    "label": {"name": "def", "description": "my cluster"},
                    "k8s_version": "1.17.0",
                    "pod_network_range": "10.192.0.0/12",
                    "service_network_range": "10.96.0.0/12",
                    "pod_dns_domain": "cluster.local",
                    "created_by_user_id": "/api/v1/user/5",
                    "created_by_user_name": "admin",
                    "created_time": 1588260014,
                    "k8shosts_config": [
                        {"node": "/api/v2/worker/k8shost/4", "role": "worker"},
                        {"node": "/api/v2/worker/k8shost/5", "role": "master"},
                    ],
                    "status": "ready",
                    "status_message": "really ready",
                    "api_endpoint_access": "api:1234",
                    "dashboard_endpoint_access": "dashboard:1234",
                    "admin_kube_config": "xyz==",
                    "dashboard_token": "abc==",
                    "persistent_storage": {"nimble_csi": False},
                },
                status_code=200,
                headers={},
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    def mocked_requests_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={
                    "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                },
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_k8scluster(self, mock_get, mock_post):

        with self.assertRaises(APIItemNotFoundException):
            get_client().k8s_cluster.get(
                k8scluster_id="/api/v2/k8scluster/999", setup_log=False
            )

        get_client().k8s_cluster.get(
            k8scluster_id="/api/v2/k8scluster/123", setup_log=False
        )

        # TODO test with setup_log = True


class TestWaitForClusterStatus(TestCase):

    # pylint: disable=no-method-argument
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v2/k8scluster/123":
            return MockResponse(
                json_data={
                    "_links": {"self": {"href": "/api/v2/k8scluster/123"}},
                    "label": {"name": "def", "description": "my cluster"},
                    "k8s_version": "1.17.0",
                    "pod_network_range": "10.192.0.0/12",
                    "service_network_range": "10.96.0.0/12",
                    "pod_dns_domain": "cluster.local",
                    "created_by_user_id": "/api/v1/user/5",
                    "created_by_user_name": "admin",
                    "created_time": 1588260014,
                    "k8shosts_config": [
                        {"node": "/api/v2/worker/k8shost/4", "role": "worker"},
                        {"node": "/api/v2/worker/k8shost/5", "role": "master"},
                    ],
                    "status": "ready",
                    "status_message": "really ready",
                    "api_endpoint_access": "api:1234",
                    "dashboard_endpoint_access": "dashboard:1234",
                    "admin_kube_config": "xyz==",
                    "dashboard_token": "abc==",
                    "persistent_storage": {"nimble_csi": False},
                },
                status_code=200,
                headers={},
            )
        if args[0] == "https://127.0.0.1:8080/api/v2/k8scluster/999":
            return MockResponse(
                json_data={}, status_code=404, raise_for_status_flag=True, headers={}
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    def mocked_requests_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={
                    "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                },
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_wait_for_status_k8scluster(self, mock_get, mock_post):

        # FIXME speed these tests up

        with self.assertRaisesRegexp(
            AssertionError, "'k8scluster_id' must be a string"
        ):
            get_client().k8s_cluster.wait_for_status(
                k8scluster_id=1, timeout_secs=1, status=[K8sClusterStatus.ready]
            )

        # pylint: disable=anomalous-backslash-in-string
        with self.assertRaisesRegexp(
            AssertionError,
            "'k8scluster_id' must have format '\/api\/v2\/worker\/k8scluster\/\[0-9\]\+'",
        ):
            get_client().k8s_cluster.wait_for_status(
                k8scluster_id="garbage", timeout_secs=1, status=[K8sClusterStatus.ready]
            )

        with self.assertRaisesRegexp(AssertionError, "'timeout_secs' must be an int"):
            get_client().k8s_cluster.wait_for_status(
                k8scluster_id="/api/v2/k8scluster/123",
                timeout_secs="blah",
                status=[K8sClusterStatus.ready],
            )

        with self.assertRaisesRegexp(AssertionError, "'timeout_secs' must be >= 0"):
            get_client().k8s_cluster.wait_for_status(
                k8scluster_id="/api/v2/k8scluster/123",
                timeout_secs=-1,
                status=[K8sClusterStatus.ready],
            )

        with self.assertRaisesRegexp(
            AssertionError, "'status' item '0' is not of type K8sClusterStatus"
        ):
            get_client().k8s_cluster.wait_for_status(
                k8scluster_id="/api/v2/k8scluster/123", timeout_secs=1, status=["abc"]
            )

        self.assertTrue(
            get_client().k8s_cluster.wait_for_status(
                k8scluster_id="/api/v2/k8scluster/123",
                timeout_secs=1,
                status=[K8sClusterStatus.ready],
            )
        )

        self.assertFalse(
            get_client().k8s_cluster.wait_for_status(
                k8scluster_id="/api/v2/k8scluster/123",
                timeout_secs=1,
                status=[K8sClusterStatus.updating],
            )
        )

        self.assertTrue(
            get_client().k8s_cluster.wait_for_status(
                k8scluster_id="/api/v2/k8scluster/123",
                timeout_secs=1,
                status=[K8sClusterStatus.ready, K8sClusterStatus.upgrading],
            )
        )

        self.assertFalse(
            get_client().k8s_cluster.wait_for_status(
                k8scluster_id="/api/v2/k8scluster/123",
                timeout_secs=1,
                status=[K8sClusterStatus.warning, K8sClusterStatus.upgrading],
            )
        )

        # Get the status of a Cluster ID that doesn't exist
        with self.assertRaises(APIItemNotFoundException):
            get_client().k8s_cluster.wait_for_status(
                k8scluster_id="/api/v2/k8scluster/999",
                timeout_secs=1,
                status=[K8sClusterStatus.ready],
            )

        # Get the status of a Cluster ID that doesn't exist - without providing a status
        with self.assertRaises(APIItemNotFoundException):
            get_client().k8s_cluster.wait_for_status(
                k8scluster_id="/api/v2/k8scluster/999", timeout_secs=1, status=[]
            )


class TestDeleteCluster(TestCase):

    # pylint: disable=no-method-argument
    def mocked_requests_delete(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v2/k8scluster/999":
            return MockResponse(
                json_data={}, status_code=404, raise_for_status_flag=True, headers={}
            )
        if args[0] == "https://127.0.0.1:8080/api/v2/k8scluster/123":
            return MockResponse(
                json_data={
                    "_links": {"self": {"href": "/api/v2/k8scluster/123"}},
                    "label": {"name": "def", "description": "my cluster"},
                    "k8s_version": "1.17.0",
                    "pod_network_range": "10.192.0.0/12",
                    "service_network_range": "10.96.0.0/12",
                    "pod_dns_domain": "cluster.local",
                    "created_by_user_id": "/api/v1/user/5",
                    "created_by_user_name": "admin",
                    "created_time": 1588260014,
                    "k8shosts_config": [
                        {"node": "/api/v2/worker/k8shost/4", "role": "worker"},
                        {"node": "/api/v2/worker/k8shost/5", "role": "master"},
                    ],
                    "status": "ready",
                    "status_message": "really ready",
                    "api_endpoint_access": "api:1234",
                    "dashboard_endpoint_access": "dashboard:1234",
                    "admin_kube_config": "xyz==",
                    "dashboard_token": "abc==",
                    "persistent_storage": {"nimble_csi": False},
                },
                status_code=200,
                headers={},
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    def mocked_requests_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={
                    "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                },
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.delete", side_effect=mocked_requests_delete)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_delete_k8scluster(self, mock_get, mock_post):

        # pylint: disable=anomalous-backslash-in-string
        with self.assertRaisesRegexp(
            AssertionError,
            "'k8scluster_id' must have format '\/api\/v2\/worker\/k8scluster\/\[0-9\]\+'",
        ):
            get_client().k8s_cluster.delete(k8scluster_id="garbage")

        with self.assertRaises(APIItemNotFoundException):
            get_client().k8s_cluster.delete(k8scluster_id="/api/v2/k8scluster/999")

        get_client().k8s_cluster.delete(k8scluster_id="/api/v2/k8scluster/123")
