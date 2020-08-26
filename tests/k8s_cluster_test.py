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

from mock import patch

from hpecp import APIException, APIItemNotFoundException
from hpecp.k8s_cluster import (
    K8sCluster,
    K8sClusterHostConfig,
    K8sClusterStatus,
)

from .base import BaseTestCase, MockResponse, get_client
from .k8s_cluster_mock_api_responses import mockApiSetup

# setup the mock data
mockApiSetup()


class TestClusterList(BaseTestCase):
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
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
        self.assertEqual(
            clusters[0].dashboard_endpoint_access, "dashboard:1234"
        )
        # The cluster wasn't created with certs
        # TODO: need a test with this value set
        self.assertIsNone(clusters[0].cert_data)
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

    # pylint: disable=no-method-argument
    def mocked_requests_get_missing_cluster_props(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v2/k8scluster":
            return MockResponse(
                json_data={
                    "_links": {"self": {"href": "/api/v2/k8scluster"}},
                    "_embedded": {
                        "k8sclusters": [
                            {
                                "_links": {
                                    "self": {"href": "/api/v2/k8scluster/20"}
                                },
                                "label": {
                                    "name": "def",
                                    "description": "my cluster",
                                },
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
                                "persistent_storage": {"nimble_csi": False},
                            }
                        ]
                    },
                },
                status_code=200,
                headers={},
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    @patch(
        "requests.get", side_effect=mocked_requests_get_missing_cluster_props
    )
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_k8sclusters_missing_props(self, mock_get, mock_post):

        # Makes GET Request: https://127.0.0.1:8080/api/v2/k8sclusters/
        clusters = get_client().k8s_cluster.list()

        # Test that json response is saved in each WorkerK8s object
        # assert client.k8s_cluster.get()[0].json is not None

        # Test WorkerK8sList subscriptable access and property setters
        self.assertEqual(clusters[0].id, "/api/v2/k8scluster/20")

        self.assertEqual(clusters[0].admin_kube_config, "")
        self.assertEqual(clusters[0].dashboard_token, "")
        self.assertEqual(clusters[0].api_endpoint_access, "")
        self.assertEqual(clusters[0].dashboard_endpoint_access, "")
        self.assertEqual(clusters[0].status_message, "")

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_k8sclusters_tabulate_all_columns(self, mock_get, mock_post):

        expected_tabulate_output = (
            "+-----------------------+------+-------------+-------------+--------+--------------------+----------------------+--------------+------------------------------------------------------------------------------------------------------------------+-------------------+-----------------+---------------------+---------------------------+-----------+--------+----------------+---------------------------------------------+\n"  # noqa: E501
            "|          id           | name | description | k8s_version | addons | created_by_user_id | created_by_user_name | created_time |                                                 k8shosts_config                                                  | admin_kube_config | dashboard_token | api_endpoint_access | dashboard_endpoint_access | cert_data | status | status_message |                   _links                    |\n"  # noqa: E501
            "+-----------------------+------+-------------+-------------+--------+--------------------+----------------------+--------------+------------------------------------------------------------------------------------------------------------------+-------------------+-----------------+---------------------+---------------------------+-----------+--------+----------------+---------------------------------------------+\n"  # noqa: E501
            '| /api/v2/k8scluster/20 | def  | my cluster  |   1.17.0    |        |   /api/v1/user/5   |        admin         |  1588260014  | [{"node": "/api/v2/worker/k8shost/4", "role": "worker"}, {"node": "/api/v2/worker/k8shost/5", "role": "master"}] |       xyz==       |      abc==      |      api:1234       |      dashboard:1234       |           | ready  |  really ready  | {"self": {"href": "/api/v2/k8scluster/20"}} |\n'  # noqa: E501
            "+-----------------------+------+-------------+-------------+--------+--------------------+----------------------+--------------+------------------------------------------------------------------------------------------------------------------+-------------------+-----------------+---------------------+---------------------------+-----------+--------+----------------+---------------------------------------------+"  # noqa: E501
        )

        # Patch k8shosts_config method to return the node attribute before the role attribute
        def new_k8shosts_config(self):
            return json.dumps(self.json["k8shosts_config"], sort_keys=True)

        setattr(K8sCluster, "k8shosts_config", property(new_k8shosts_config))

        k8scluster_list = get_client().k8s_cluster.list()

        self.maxDiff = None
        self.assertEqual(
            k8scluster_list.tabulate().replace("'", '"'),
            expected_tabulate_output,
        )  # noqa: E501

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_k8sclusters_tabulate_with_column_list(self, mock_get, mock_post):

        k8scluster_list = get_client().k8s_cluster.list()
        self.assertEqual(
            k8scluster_list.tabulate(["description", "id"]),
            "+-------------+-----------------------+\n"
            "| description |          id           |\n"
            "+-------------+-----------------------+\n"
            "| my cluster  | /api/v2/k8scluster/20 |\n"
            "+-------------+-----------------------+",
        )


class TestCreateCluster(TestCase):
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
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
            get_client().k8s_cluster.create(
                name="a", persistent_storage_local=1
            )

        with self.assertRaisesRegexp(
            AssertionError,
            "'persistent_storage_nimble_csi' must be True or False",
        ):
            get_client().k8s_cluster.create(
                name="a", persistent_storage_nimble_csi=1
            )

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
            (
                "'node' must have format"
                " '\/api\/v2\/worker\/k8shost\/\[0-9\]\+'"  # noqa: W605
            ),
        ):
            get_client().k8s_cluster.create(
                name="a", k8shosts_config=[K8sClusterHostConfig("a", "b")]
            )

        with self.assertRaisesRegexp(
            AssertionError,
            "'role' must one of \['master, worker'\]",  # noqa: W605
        ):
            get_client().k8s_cluster.create(
                name="a",
                k8shosts_config=[
                    K8sClusterHostConfig("/api/v2/worker/k8shost/1", "b")
                ],
            )

        # Finally we can create a cluster
        id = get_client().k8s_cluster.create(
            name="a",
            k8shosts_config=[
                K8sClusterHostConfig("/api/v2/worker/k8shost/1", "master")
            ],
        )
        self.assertEqual(id, "/api/v2/k8scluster/99")

        # now with a description
        id = get_client().k8s_cluster.create(
            name="a",
            k8shosts_config=[
                K8sClusterHostConfig("/api/v2/worker/k8shost/1", "master")
            ],
            description="Cluster Description",
        )
        self.assertEqual(id, "/api/v2/k8scluster/99")

        # now with a k8s version
        id = get_client().k8s_cluster.create(
            name="a",
            k8shosts_config=[
                K8sClusterHostConfig("/api/v2/worker/k8shost/1", "master")
            ],
            k8s_version="1.18.0",
        )
        self.assertEqual(id, "/api/v2/k8scluster/99")

        # now with a k8s version
        id = get_client().k8s_cluster.create(
            name="a",
            k8shosts_config=[
                K8sClusterHostConfig("/api/v2/worker/k8shost/1", "master")
            ],
            k8s_version="1.18.0",
            addons=["picasso"],
        )
        self.assertEqual(id, "/api/v2/k8scluster/99")

    def mocked_requests_create_error_post(*args, **kwargs):
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
        elif args[0] == "https://127.0.0.1:8080/api/v2/k8scluster":
            return MockResponse(
                json_data={},
                raise_for_status_flag=True,
                status_code=500,
                headers={},
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
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_k8scluster(self, mock_get, mock_post):

        with self.assertRaises(APIItemNotFoundException):
            get_client().k8s_cluster.get(
                id="/api/v2/k8scluster/999", setup_log=False
            )

        get_client().k8s_cluster.get(
            id="/api/v2/k8scluster/123", setup_log=False
        )

        get_client().k8s_cluster.get(
            id="/api/v2/k8scluster/123", setup_log=True
        )


class TestWaitForClusterStatus(BaseTestCase):

    # pylint: disable=no-method-argument
    # def mocked_requests_get(*args, **kwargs):
    #     if args[0] == "https://127.0.0.1:8080/api/v2/k8scluster/123":
    #         return MockResponse(
    #             json_data={
    #                 "_links": {"self": {"href": "/api/v2/k8scluster/123"}},
    #                 "label": {"name": "def", "description": "my cluster"},
    #                 "k8s_version": "1.17.0",
    #                 "pod_network_range": "10.192.0.0/12",
    #                 "service_network_range": "10.96.0.0/12",
    #                 "pod_dns_domain": "cluster.local",
    #                 "created_by_user_id": "/api/v1/user/5",
    #                 "created_by_user_name": "admin",
    #                 "created_time": 1588260014,
    #                 "k8shosts_config": [
    #                     {"node": "/api/v2/worker/k8shost/4", "role": "worker"},
    #                     {"node": "/api/v2/worker/k8shost/5", "role": "master"},
    #                 ],
    #                 "status": "ready",
    #                 "status_message": "really ready",
    #                 "api_endpoint_access": "api:1234",
    #                 "dashboard_endpoint_access": "dashboard:1234",
    #                 "admin_kube_config": "xyz==",
    #                 "dashboard_token": "abc==",
    #                 "persistent_storage": {"nimble_csi": False},
    #             },
    #             status_code=200,
    #             headers={},
    #         )
    #     if (
    #         args[0]
    #         == "https://127.0.0.1:8080/api/v2/k8scluster/123?setup_log=true"
    #     ):
    #         return MockResponse(
    #             json_data={
    #                 "_links": {"self": {"href": "/api/v2/k8scluster/123"}},
    #                 "label": {"name": "def", "description": "my cluster"},
    #                 "k8s_version": "1.17.0",
    #                 "pod_network_range": "10.192.0.0/12",
    #                 "service_network_range": "10.96.0.0/12",
    #                 "pod_dns_domain": "cluster.local",
    #                 "created_by_user_id": "/api/v1/user/5",
    #                 "created_by_user_name": "admin",
    #                 "created_time": 1588260014,
    #                 "k8shosts_config": [
    #                     {"node": "/api/v2/worker/k8shost/4", "role": "worker"},
    #                     {"node": "/api/v2/worker/k8shost/5", "role": "master"},
    #                 ],
    #                 "status": "ready",
    #                 "status_message": "really ready",
    #                 "api_endpoint_access": "api:1234",
    #                 "dashboard_endpoint_access": "dashboard:1234",
    #                 "admin_kube_config": "xyz==",
    #                 "dashboard_token": "abc==",
    #                 "persistent_storage": {"nimble_csi": False},
    #             },
    #             status_code=200,
    #             headers={},
    #         )
    #     if args[0] == "https://127.0.0.1:8080/api/v2/k8scluster/999":
    #         return MockResponse(
    #             json_data={},
    #             status_code=404,
    #             raise_for_status_flag=True,
    #             headers={},
    #         )
    #     if (
    #         args[0]
    #         == "https://127.0.0.1:8080/api/v2/k8scluster/999?setup_log=true"
    #     ):
    #         return MockResponse(
    #             json_data={},
    #             status_code=404,
    #             raise_for_status_flag=True,
    #             headers={},
    #         )
    #     raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_wait_for_status_k8scluster_assertions(self, mock_get, mock_post):

        # FIXME speed these tests up

        with self.assertRaisesRegexp(
            AssertionError, "'id' must be provided and must be a str"
        ):
            get_client().k8s_cluster.wait_for_status(
                id=1,
                timeout_secs=1,
                status=[K8sClusterStatus.ready],
            )

        # pylint: disable=anomalous-backslash-in-string
        with self.assertRaisesRegexp(
            AssertionError,
            "'id' does not start with '/api/v2/k8scluster'",
        ):
            get_client().k8s_cluster.wait_for_status(
                id="garbage",
                timeout_secs=1,
                status=[K8sClusterStatus.ready],
            )

        with self.assertRaisesRegexp(
            AssertionError, "'timeout_secs' must be an int"
        ):
            get_client().k8s_cluster.wait_for_status(
                id="/api/v2/k8scluster/123",
                timeout_secs="blah",
                status=[K8sClusterStatus.ready],
            )

        with self.assertRaisesRegexp(
            AssertionError, "'timeout_secs' must be >= 0"
        ):
            get_client().k8s_cluster.wait_for_status(
                id="/api/v2/k8scluster/123",
                timeout_secs=-1,
                status=[K8sClusterStatus.ready],
            )

        with self.assertRaisesRegexp(
            AssertionError,
            "'status' item '0' is not of type <enum 'K8sClusterStatus'>",
        ):
            get_client().k8s_cluster.wait_for_status(
                id="/api/v2/k8scluster/123",
                timeout_secs=1,
                status=["abc"],
            )

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_wait_for_status_k8scluster_body(self, mock_get, mock_post):

        self.assertTrue(
            get_client().k8s_cluster.wait_for_status(
                id="/api/v2/k8scluster/123",
                timeout_secs=1,
                status=[K8sClusterStatus.ready],
            )
        )

        self.assertFalse(
            get_client().k8s_cluster.wait_for_status(
                id="/api/v2/k8scluster/123",
                timeout_secs=1,
                status=[K8sClusterStatus.updating],
            )
        )

        self.assertTrue(
            get_client().k8s_cluster.wait_for_status(
                id="/api/v2/k8scluster/123",
                timeout_secs=1,
                status=[K8sClusterStatus.ready, K8sClusterStatus.upgrading],
            )
        )

        self.assertFalse(
            get_client().k8s_cluster.wait_for_status(
                id="/api/v2/k8scluster/123",
                timeout_secs=1,
                status=[K8sClusterStatus.warning, K8sClusterStatus.upgrading],
            )
        )

        # Get the status of a Cluster ID that doesn't exist
        with self.assertRaises(APIItemNotFoundException):
            get_client().k8s_cluster.wait_for_status(
                id="/api/v2/k8scluster/999",
                timeout_secs=1,
                status=[K8sClusterStatus.ready],
            )

        # Get the status of a Cluster ID that doesn't exist
        # without providing a status
        self.assertTrue(
            get_client().k8s_cluster.wait_for_status(
                id="/api/v2/k8scluster/999",
                timeout_secs=1,
                status=[],
            )
        )


class TestDeleteCluster(BaseTestCase):

    non_existent_cluster_url = "/api/v2/k8scluster/999"

    existing_cluster_url = "/api/v2/k8scluster/123"

    # pylint: disable=no-method-argument

    @patch("requests.delete", side_effect=BaseTestCase.httpDeleteHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_delete_k8scluster(self, mock_get, mock_post):

        # pylint: disable=anomalous-backslash-in-string
        with self.assertRaisesRegexp(
            AssertionError,
            ("'id' does not start with '/api/v2/k8scluster'"),
        ):
            get_client().k8s_cluster.delete(id="garbage")

        with self.assertRaises(APIItemNotFoundException):
            get_client().k8s_cluster.delete(
                id=TestDeleteCluster.non_existent_cluster_url
            )

        get_client().k8s_cluster.delete(
            id=TestDeleteCluster.existing_cluster_url
        )

    @patch("requests.delete", side_effect=BaseTestCase.httpDeleteHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_delete_k8scluster_cli(self, mock_delete, mock_get):

        try:
            hpecp = self.cli.CLI()
            hpecp.k8scluster.delete(id=TestDeleteCluster.existing_cluster_url)

            self.maxDiff = None

            output = self.out.getvalue().strip()
            self.assertEqual(output, "")

            # FIXME: This is failing on Python 3x because stderr seems to contain
            #        the unitest framework output.

            # error = self.err.getvalue().strip()
            # self.assertEqual(error, "")

        except Exception:
            self.fail("Unexpected exception.")

    @patch("requests.delete", side_effect=BaseTestCase.httpDeleteHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_delete_k8scluster_cli_with_exception(self, mock_delete, mock_get):

        with self.assertRaises(SystemExit) as cm:
            hpecp = self.cli.CLI()
            hpecp.k8scluster.delete(
                id=TestDeleteCluster.non_existent_cluster_url
            )

            self.maxDiff = None

            output = self.out.getvalue().strip()
            self.assertEqual(output, "")

            error = self.err.getvalue().strip()
            self.assertEqual(error, "'/api/v2/k8scluster/999' does not exist")

            self.assertEqual(cm.exception.code, 1)


class TestK8sSupportVersions(BaseTestCase):

    # # pylint: disable=no-method-argument
    # def mocked_requests_get(*args, **kwargs):
    #     if args[0] == "https://127.0.0.1:8080/api/v2/k8smanifest":
    #         return MockResponse(
    #             json_data={
    #                 "_version": "1.0",
    #                 "supported_versions": [
    #                     "1.14.10",
    #                     "1.15.7",
    #                     "1.16.4",
    #                     "1.17.0",
    #                     "1.18.0",
    #                 ],
    #                 "version_info": {
    #                     "1.14.10": {
    #                         "_version": "1.0",
    #                         "min_upgrade_version": "1.13.0",
    #                         "relnote_url": (
    #                             "https://v1-14.docs.kubernetes.io/docs/setup"
    #                             "/release/notes/"
    #                         ),
    #                         "hpecsi": "1.14",
    #                     },
    #                     "1.15.7": {
    #                         "_version": "1.0",
    #                         "min_upgrade_version": "1.14.0",
    #                         "relnote_url": (
    #                             "https://v1-15.docs.kubernetes.io/docs/setup"
    #                             "/release/notes/"
    #                         ),
    #                         "hpecsi": "1.15",
    #                     },
    #                     "1.16.4": {
    #                         "_version": "1.0",
    #                         "min_upgrade_version": "1.15.0",
    #                         "relnote_url": (
    #                             "https://v1-16.docs.kubernetes.io/docs/setup"
    #                             "/release/notes/"
    #                         ),
    #                         "hpecsi": "1.16",
    #                     },
    #                     "1.17.0": {
    #                         "_version": "1.0",
    #                         "min_upgrade_version": "1.16.0",
    #                         "relnote_url": (
    #                             "https://v1-17.docs.kubernetes.io/docs/setup"
    #                             "/release/notes/"
    #                         ),
    #                         "hpecsi": "1.17",
    #                     },
    #                     "1.18.0": {
    #                         "_version": "1.0",
    #                         "min_upgrade_version": "1.17.0",
    #                         "relnote_url": (
    #                             "https://kubernetes.io/docs/setup"
    #                             "/release/notes/"
    #                         ),
    #                         "hpecsi": "1.18",
    #                     },
    #                 },
    #             },
    #             status_code=200,
    #             headers={},
    #         )
    #     raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_k8s_supported_versions(self, mock_get, mock_post):

        self.assertEquals(
            get_client().k8s_cluster.k8s_supported_versions(),
            ["1.14.10", "1.15.7", "1.16.4", "1.17.0", "1.17.1", "1.18.0"],
        )


class TestCLI(BaseTestCase):

    # pylint: disable=no-method-argument
    # def mocked_requests_get(*args, **kwargs):
    # if args[0] == "https://127.0.0.1:8080/api/v2/k8scluster":
    #     return MockResponse(
    #         json_data={
    #             "_links": {"self": {"href": "/api/v2/k8scluster"}},
    #             "_embedded": {
    #                 "k8sclusters": [
    #                     {
    #                         "_links": {
    #                             "self": {"href": "/api/v2/k8scluster/20"}
    #                         },
    #                         "label": {
    #                             "name": "def",
    #                             "description": "my cluster",
    #                         },
    #                         "k8s_version": "1.17.0",
    #                         "pod_network_range": "10.192.0.0/12",
    #                         "service_network_range": "10.96.0.0/12",
    #                         "pod_dns_domain": "cluster.local",
    #                         "created_by_user_id": "/api/v1/user/5",
    #                         "created_by_user_name": "admin",
    #                         "created_time": 1588260014,
    #                         "k8shosts_config": [
    #                             {
    #                                 "node": "/api/v2/worker/k8shost/4",
    #                                 "role": "worker",
    #                             },
    #                             {
    #                                 "node": "/api/v2/worker/k8shost/5",
    #                                 "role": "master",
    #                             },
    #                         ],
    #                         "status": "ready",
    #                         "status_message": "really ready",
    #                         "api_endpoint_access": "api:1234",
    #                         "dashboard_endpoint_access": "dashboard:1234",
    #                         "admin_kube_config": "xyz==",
    #                         "dashboard_token": "abc==",
    #                         "persistent_storage": {"nimble_csi": False},
    #                     }
    #                 ]
    #             },
    #         },
    #         status_code=200,
    #         headers={},
    #     )
    # if args[0] == "https://127.0.0.1:8080/api/v2/k8smanifest":
    #     return MockResponse(
    #         json_data={
    #             "_version": "1.0",
    #             "supported_versions": [
    #                 "1.14.10",
    #                 "1.15.7",
    #                 "1.16.4",
    #                 "1.17.0",
    #                 "1.17.1",
    #                 "1.18.0",
    #             ],
    #             "version_info": {
    #                 "1.14.10": {
    #                     "_version": "1.0",
    #                     "min_upgrade_version": "1.13.0",
    #                     "relnote_url": (
    #                         "https://v1-14.docs.kubernetes.io/docs/setup"
    #                         "/release/notes/"
    #                     ),
    #                     "hpecsi": "1.14",
    #                 },
    #                 "1.15.7": {
    #                     "_version": "1.0",
    #                     "min_upgrade_version": "1.14.0",
    #                     "relnote_url": (
    #                         "https://v1-15.docs.kubernetes.io/docs/setup"
    #                         "/release/notes/"
    #                     ),
    #                     "hpecsi": "1.15",
    #                 },
    #                 "1.16.4": {
    #                     "_version": "1.0",
    #                     "min_upgrade_version": "1.15.0",
    #                     "relnote_url": (
    #                         "https://v1-16.docs.kubernetes.io/docs/setup"
    #                         "/release/notes/"
    #                     ),
    #                     "hpecsi": "1.16",
    #                 },
    #                 "1.17.0": {
    #                     "_version": "1.0",
    #                     "min_upgrade_version": "1.16.0",
    #                     "relnote_url": (
    #                         "https://v1-17.docs.kubernetes.io/docs/setup"
    #                         "/release/notes/"
    #                     ),
    #                     "hpecsi": "1.17",
    #                 },
    #                 "1.17.1": {
    #                     "_version": "1.0",
    #                     "min_upgrade_version": "1.17.0",
    #                     "relnote_url": (
    #                         "https://v1-17.docs.kubernetes.io/docs/setup"
    #                         "/release/notes/"
    #                     ),
    #                     "hpecsi": "1.17",
    #                 },
    #                 "1.18.0": {
    #                     "_version": "1.0",
    #                     "min_upgrade_version": "1.17.0",
    #                     "relnote_url": (
    #                         "https://kubernetes.io/docs/setup"
    #                         "/release/notes/"
    #                     ),
    #                     "hpecsi": "1.18",
    #                 },
    #             },
    #         },
    #         status_code=200,
    #         headers={},
    #     )
    # raise RuntimeError("Unhandle GET request: " + args[0])

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8scluster_list(self, mock_post, mock_get):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.list(columns=["id", "name", "description", "status"])

        output = self.out.getvalue().strip()
        self.assertEqual(
            output,
            (
                "+-----------------------+------+-------------+--------+\n"
                "|          id           | name | description | status |\n"
                "+-----------------------+------+-------------+--------+\n"
                "| /api/v2/k8scluster/20 | def  | my cluster  | ready  |\n"
                "+-----------------------+------+-------------+--------+"
            ),
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_no_filter(self, mock_post, mock_get):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.k8s_supported_versions()

        output = self.out.getvalue().strip()
        self.assertEqual(
            output,
            "['1.14.10', '1.15.7', '1.16.4', '1.17.0', '1.17.1', '1.18.0']",
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_no_filter_output_json(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.k8s_supported_versions(output="json")

        output = self.out.getvalue().strip()
        self.assertEqual(
            output,
            "['1.14.10', '1.15.7', '1.16.4', '1.17.0', '1.17.1', '1.18.0']",
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_no_filter_output_text(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.k8s_supported_versions(output="text")

        output = self.out.getvalue().strip()
        self.assertEqual(
            output,
            "1.14.10 1.15.7 1.16.4 1.17.0 1.17.1 1.18.0",
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_no_filter_output_invalid(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()

        with self.assertRaises(SystemExit) as cm:
            hpecp.k8scluster.k8s_supported_versions(output="garbage")

        self.assertEqual(cm.exception.code, 1)

        output = self.out.getvalue().strip()
        self.assertEqual(
            output,
            "",
        )

        error = self.err.getvalue().strip()
        self.assertEqual(
            error,
            "'output' parameter ust be 'json' or 'text'",
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_major_filter_match(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.k8s_supported_versions(major_filter=1)

        output = self.out.getvalue().strip()
        self.assertEqual(
            output,
            "['1.14.10', '1.15.7', '1.16.4', '1.17.0', '1.17.1', '1.18.0']",
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_major_filter_no_match(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.k8s_supported_versions(major_filter=2)

        output = self.out.getvalue().strip()
        self.assertEqual(
            output,
            "[]",
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_minor_filter_match(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.k8s_supported_versions(minor_filter=17)

        output = self.out.getvalue().strip()
        self.assertEqual(
            output,
            "['1.17.0', '1.17.1']",
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_minor_filter_no_match(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.k8s_supported_versions(minor_filter=2)

        output = self.out.getvalue().strip()
        self.assertEqual(
            output,
            "[]",
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_patch_filter_match(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.k8s_supported_versions(patch_filter=0)

        output = self.out.getvalue().strip()
        self.assertEqual(
            output,
            "['1.17.0', '1.18.0']",
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_patch_filter_no_match(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.k8s_supported_versions(patch_filter=21)

        output = self.out.getvalue().strip()
        self.assertEqual(
            output,
            "[]",
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_major_filter_invalid(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()
        with self.assertRaises(SystemExit) as cm:
            hpecp.k8scluster.k8s_supported_versions(major_filter="text")

        output = self.out.getvalue().strip()
        self.assertEqual(output, "")

        error = self.err.getvalue().strip()
        self.assertEqual(error, "'major_filter' if provided must be an int")

        self.assertEqual(cm.exception.code, 1)

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_minor_filter_invalid(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()
        with self.assertRaises(SystemExit) as cm:
            hpecp.k8scluster.k8s_supported_versions(minor_filter="text")

        output = self.out.getvalue().strip()
        self.assertEqual(output, "")

        error = self.err.getvalue().strip()
        self.assertEqual(error, "'minor_filter' if provided must be an int")

        self.assertEqual(cm.exception.code, 1)

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    def test_k8s_supported_verions_patch_filter_invalid(
        self, mock_post, mock_get
    ):

        hpecp = self.cli.CLI()
        with self.assertRaises(SystemExit) as cm:
            hpecp.k8scluster.k8s_supported_versions(patch_filter="text")

        output = self.out.getvalue().strip()
        self.assertEqual(output, "")

        error = self.err.getvalue().strip()
        self.assertEqual(error, "'patch_filter' if provided must be an int")

        self.assertEqual(cm.exception.code, 1)

    def mocked_requests_create_post(*args, **kwargs):
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
        elif args[0] == "https://127.0.0.1:8080/api/v2/k8scluster":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={"Location": "/api/v2/k8sclusters/99"},
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_create_post)
    def test_k8scluster_create(self, mock_post):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.create(
            name="mycluster",
            k8shosts_config="/api/v2/worker/k8shost/1:master,/api/v2/worker/k8shost/2:worker",
        )

        output = self.out.getvalue().strip()
        self.assertEqual(output, "/api/v2/k8sclusters/99")

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_k8scluster_admin_kube_config(self, mock_get, mock_post):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.admin_kube_config(id="/api/v2/k8scluster/123")

        output = self.out.getvalue().strip()
        self.assertEqual(output, "test_admin_kube_config")

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_k8scluster_dashboard_url(self, mock_get, mock_post):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.dashboard_url(id="/api/v2/k8scluster/123")

        output = self.out.getvalue().strip()
        self.assertEqual(output, "test_dashboard_url")

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_k8scluster_dashboard_token(self, mock_get, mock_post):

        hpecp = self.cli.CLI()
        hpecp.k8scluster.dashboard_token(id="/api/v2/k8scluster/123")

        output = self.out.getvalue().strip()
        self.assertEqual(output, "abc")  # abc base64 encoded is: YWJjCg==


class TestCliStates(BaseTestCase):
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_states(self, mock_post):

        self.maxDiff = None

        hpecp = self.cli.CLI()
        hpecp.k8scluster.statuses()
        stdout = self.out.getvalue().strip()

        expected_stdout = str(
            [
                "ready",
                "creating",
                "updating",
                "upgrading",
                "deleting",
                "error",
                "warning",
            ]
        )

        self.assertEqual(stdout, expected_stdout)


class TestK8sClusterHostConfig(TestCase):
    def test_cluster_host_config(self):

        expected_error = "'noderole' list must have two values [ node, role ]"
        try:
            K8sClusterHostConfig.create_from_list(noderole=[1, 2, 3])
        except AssertionError as e:
            self.assertEquals(
                e.args[0],
                expected_error,
            )

        conf = K8sClusterHostConfig.create_from_list(
            noderole=["/api/v2/worker/k8shost/1", "master"]
        )
        self.assertIsInstance(conf, K8sClusterHostConfig)
