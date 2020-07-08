from unittest import TestCase
import requests
from mock import patch

from hpecp import ContainerPlatformClient
from hpecp.k8s_worker import K8sWorkerController, WorkerK8sStatus
from hpecp.exceptions import APIItemConflictException, APIItemNotFoundException
from .base_test import session_mock_response, BaseTestCase
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


class TestWorkers(TestCase):
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v2/worker/k8shost":
            return MockResponse(
                json_data={
                    "_embedded": {
                        "k8shosts": [
                            {
                                "status": "unlicensed",
                                "propinfo": {
                                    "bds_storage_apollo": "false",
                                    "bds_network_publicinterface": "ens5",
                                },
                                "approved_worker_pubkey": [],
                                "tags": [],
                                "hostname": (
                                    "ip-10-1-0-238.eu-west-2.compute.internal"
                                ),
                                "ipaddr": "10.1.0.238",
                                "setup_log": (
                                    "/var/log/bluedata/install/"
                                    "k8shost_setup_10.1.0.238-"
                                    "2020-4-26-18-41-16"
                                ),
                                "_links": {
                                    "self": {
                                        "href": "/api/v2/worker/k8shost/4"
                                    }
                                },
                                "sysinfo": {
                                    "network": [],
                                    "keys": {
                                        "reported_worker_public_key": (
                                            "ssh-rsa ...== server\n"
                                        )
                                    },
                                    "storage": [],
                                    "swap": {"swap_total": 0},
                                    "memory": {"mem_total": 65842503680},
                                    "gpu": {"gpu_count": 0},
                                    "cpu": {
                                        "cpu_logical_cores": 16,
                                        "cpu_count": 8,
                                        "cpu_physical_cores": 8,
                                        "cpu_sockets": 1,
                                    },
                                    "mountpoint": [],
                                },
                            },
                            {
                                "status": "bundle",
                                "approved_worker_pubkey": [],
                                "tags": [],
                                "hostname": "",
                                "ipaddr": "10.1.0.186",
                                "setup_log": (
                                    "/var/log/bluedata/install/"
                                    "k8shost_setup_10.1.0.186-"
                                    "2020-4-26-18-49-10"
                                ),
                                "_links": {
                                    "self": {
                                        "href": "/api/v2/worker/k8shost/5"
                                    }
                                },
                            },
                        ]
                    }
                },
                status_code=200,
                headers={},
            )
        elif args[0] == "https://127.0.0.1:8080/api/v2/worker/k8shost/5":
            return MockResponse(
                json_data={
                    "status": "bundle",
                    "approved_worker_pubkey": [],
                    "tags": [],
                    "hostname": "",
                    "ipaddr": "10.1.0.186",
                    "setup_log": (
                        "/var/log/bluedata/install/"
                        "k8shost_setup_10.1.0.186-"
                        "2020-4-26-18-49-10"
                    ),
                    "_links": {"self": {"href": "/api/v2/worker/k8shost/5"}},
                },
                status_code=200,
                headers={},
            )
        elif args[0] == "https://127.0.0.1:8080/api/v2/worker/k8shost/8":
            return MockResponse(
                json_data={},
                status_code=404,
                raise_for_status_flag=True,
                headers={},
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

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
        elif args[0] == "https://127.0.0.1:8080/api/v2/worker/k8shost/5":
            return MockResponse(json_data={}, status_code=204, headers={})

        raise RuntimeError("Unhandled POST request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_k8shosts(self, mock_get, mock_post):

        client = get_client()

        # Makes GET Request: https://127.0.0.1:8080/api/v2/worker/k8shost/
        workers = client.k8s_worker.list()

        # Test that json response is saved in each WorkerK8s object
        assert client.k8s_worker.list()[0].json is not None

        # Test WorkerK8sList subscriptable access and property setters
        assert workers[0].worker_id == 4
        assert workers[0].status == WorkerK8sStatus.unlicensed.name
        assert (
            workers[0].hostname == "ip-10-1-0-238.eu-west-2.compute.internal"
        )
        assert workers[0].ipaddr == "10.1.0.238"
        assert workers[0].href == "/api/v2/worker/k8shost/4"

        # Test WorkerK8sList iterators
        assert [worker.worker_id for worker in client.k8s_worker.list()] == [
            4,
            5,
        ]

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_set_storage_invalid_worker_id(self, mock_get, mock_post):
        client = get_client()
        with self.assertRaisesRegexp(
            AssertionError,
            "'id' does not start with '/api/v2/worker/k8shost'",
        ):
            client.k8s_worker.set_storage(worker_id="garbage")

        with self.assertRaises(AssertionError):
            client.k8s_worker.set_storage(worker_id=123)

        with self.assertRaises(APIItemNotFoundException):
            client.k8s_worker.set_storage(worker_id="/api/v2/worker/k8shost/8")

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_set_storage_no_disks(self, mock_get, mock_post):
        client = get_client()

        with self.assertRaises(AssertionError) as c:
            client.k8s_worker.set_storage(worker_id="/api/v2/worker/k8shost/5")
        self.assertEqual(
            str(c.exception),
            "'ephemeral_disks' must contain at least one disk",
        )

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_set_storage_invalid_ephemeral_disks(self, mock_get, mock_post):
        client = get_client()

        with self.assertRaises(AssertionError) as c:
            client.k8s_worker.set_storage(
                worker_id="/api/v2/worker/k8shost/5",
                ephemeral_disks="garbage",
            )
        self.assertEqual(
            str(c.exception),
            "'ephemeral_disks' must be provided and and must be a list",
        )

        with self.assertRaises(AssertionError) as c:
            client.k8s_worker.set_storage(
                worker_id="/api/v2/worker/k8shost/5", ephemeral_disks=list()
            )
        self.assertEqual(
            str(c.exception),
            "'ephemeral_disks' must contain at least one disk",
        )

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_set_storage_invalid_persistent_disks(self, mock_get, mock_post):
        client = get_client()
        _sample_ep_disks = ["/dev/nvme2n1", "/dev/nvme2n2"]

        with self.assertRaises(AssertionError) as c:
            client.k8s_worker.set_storage(
                worker_id="/api/v2/worker/k8shost/5",
                ephemeral_disks=_sample_ep_disks,
                persistent_disks="garbage",
            )
        self.assertEqual(str(c.exception), "'persistent_disks' must be a list")

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_set_storage_only_ephemeral_disks(self, mock_get, mock_post):
        client = get_client()

        _sample_ep_disks = ["/dev/nvme2n1", "/dev/nvme2n2"]
        client.k8s_worker.set_storage(
            worker_id="/api/v2/worker/k8shost/5",
            ephemeral_disks=_sample_ep_disks,
        )


class TestCliCreate(BaseTestCase):
    def test_key_or_keycontent_provided(self,):

        hpecp = self.cli.CLI()
        with self.assertRaises(SystemExit) as cm:
            hpecp.k8sworker.create_with_ssh_key(ip="127.0.0.1")

        self.assertEqual(cm.exception.code, 1)

        actual_err = self.err.getvalue().strip()
        expected_err = "Either ssh_key or ssh_key_file must be provided"

        self.assertEqual(self.out.getvalue(), "", "stdout should be empty")

        self.assertTrue(
            actual_err.endswith(expected_err),
            "Actual stderr: `{}` Expected stderr: `{}`".format(
                actual_err, expected_err
            ),
        )

    def test_key_and_keycontent_provided(self,):

        hpecp_cli = self.cli.CLI()
        with self.assertRaises(SystemExit) as cm:
            hpecp_cli.k8sworker.create_with_ssh_key(
                ip="127.0.0.1", ssh_key="foobar", ssh_key_file="foobar"
            )

        self.assertEqual(cm.exception.code, 1)

        actual_err = self.err.getvalue().strip()
        expected_err = "Either ssh_key or ssh_key_file must be provided"

        self.assertEqual(self.out.getvalue(), "", "stdout should be empty")

        self.assertTrue(
            actual_err.endswith(expected_err),
            "Actual stderr: `{}` Expected stderr: `{}`".format(
                actual_err, expected_err
            ),
        )

    def mocked_requests_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return session_mock_response()
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("hpecp.k8s_worker")
    def test_with_only_ssh_key_content_provided(
        self, mock_post, mock_k8sworker
    ):

        """Test that the ssh key content provided by the 'ssh_key' parameter
        is passed to the library method 'create_with_ssh_key()'.
        """

        with patch.object(
            K8sWorkerController,
            "create_with_ssh_key",
            return_value="/api/v2/worker/k8shost/1",
        ) as mock_create_with_ssh_key:
            try:
                hpecp_cli = self.cli.CLI()
                hpecp_cli.k8sworker.create_with_ssh_key(
                    ip="127.0.0.1", ssh_key="test_ssh_key",
                )
            except Exception:
                self.fail("Unexpected exception.")

        mock_create_with_ssh_key.assert_called_once_with(
            ip="127.0.0.1", ssh_key_data="test_ssh_key", tags=[],
        )

        stdout = self.out.getvalue().strip()

        self.assertEqual(stdout, "/api/v2/worker/k8shost/1")

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("hpecp.k8s_worker")
    def test_with_only_ssh_key_content_provided_raises_assertion_error(
        self, mock_post, mock_k8sworker
    ):

        with patch.object(
            K8sWorkerController,
            "create_with_ssh_key",
            side_effect=AssertionError("TEST_ASSERTION"),
        ):
            with self.assertRaises(SystemExit) as cm:
                hpecp_cli = self.cli.CLI()
                hpecp_cli.k8sworker.create_with_ssh_key(
                    ip="127.0.0.1", ssh_key="test_ssh_key",
                )

        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_err = "TEST_ASSERTION"

        self.assertEqual(stdout, "")
        self.assertTrue(
            stderr.endswith(expected_err),
            "Expected: `{}`, Actual: `{}`".format(expected_err, stderr),
        )

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("hpecp.k8s_worker")
    def test_with_only_ssh_key_content_provided_raises_conflict_exception(
        self, mock_post, mock_k8sworker
    ):

        with patch.object(
            K8sWorkerController,
            "create_with_ssh_key",
            side_effect=APIItemConflictException(
                message="MESSAGE", request_method="METHOD", request_url="URL",
            ),
        ):
            with self.assertRaises(SystemExit) as cm:
                hpecp_cli = self.cli.CLI()
                hpecp_cli.k8sworker.create_with_ssh_key(
                    ip="127.0.0.1", ssh_key="test_ssh_key",
                )

        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_err = "Worker already exists."

        self.assertEqual(stdout, "")
        self.assertTrue(
            stderr.endswith(expected_err),
            "Expected: `{}`, Actual: `{}`".format(expected_err, stderr),
        )

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("hpecp.k8s_worker")
    def test_with_only_ssh_key_content_provided_raises_general_exception(
        self, mock_post, mock_k8sworker
    ):

        with patch.object(
            K8sWorkerController,
            "create_with_ssh_key",
            side_effect=Exception("TEST_EXCEPTION"),
        ):
            with self.assertRaises(SystemExit) as cm:
                hpecp_cli = self.cli.CLI()
                hpecp_cli.k8sworker.create_with_ssh_key(
                    ip="127.0.0.1", ssh_key="test_ssh_key",
                )

        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_err = (
            "Unknown error. To debug run with env var LOG_LEVEL=DEBUG"
        )

        self.assertEqual(stdout, "")
        self.assertTrue(
            stderr.endswith(expected_err),
            "Expected: `{}`, Actual: `{}`".format(expected_err, stderr),
        )

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("hpecp.k8s_worker")
    def test_with_only_ssh_key_file_provided(self, mock_post, mock_k8sworker):

        ssh_key_file = tempfile.NamedTemporaryFile(delete=True, mode="w")
        ssh_key_file.write("test_ssh_key_file_data")
        ssh_key_file.flush()

        with patch.object(
            K8sWorkerController,
            "create_with_ssh_key",
            return_value="/api/v2/worker/k8shost/1",
        ) as mock_create_with_ssh_key:
            try:
                hpecp_cli = self.cli.CLI()
                hpecp_cli.k8sworker.create_with_ssh_key(
                    ip="127.0.0.1", ssh_key_file=ssh_key_file.name,
                )
            except Exception as e:
                self.fail("Unexpected exception. {}".format(e))

        mock_create_with_ssh_key.assert_called_once_with(
            ip="127.0.0.1", ssh_key_data="test_ssh_key_file_data", tags=[],
        )

        stdout = self.out.getvalue().strip()

        self.assertEqual(stdout, "/api/v2/worker/k8shost/1")

        ssh_key_file.close()
