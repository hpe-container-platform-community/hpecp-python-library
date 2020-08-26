import tempfile

from mock import patch

from hpecp import ContainerPlatformClient
from hpecp.cli import base
from hpecp.exceptions import APIItemConflictException, APIItemNotFoundException
from hpecp.k8s_worker import K8sWorkerController, WorkerK8s, WorkerK8sStatus

from .base import BaseTestCase, get_client
from .k8s_worker_mock_api_responses import mockApiSetup

# setup the mock data
mockApiSetup()


class TestWorkers(BaseTestCase):
    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_create_with_ssh_key_data(self, mock_get, mock_post):

        client = get_client()

        # Makes GET Request: https://127.0.0.1:8080/api/v2/worker/k8shost/
        worker_id = client.k8s_worker.create_with_ssh_key(
            ip="127.0.0.1", ssh_key_data="test ssh key"
        )

        self.assertEqual(worker_id, "/new/cluster/id")

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
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

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_k8shosts_with_setup_log(self, mock_get, mock_post):

        client = get_client()
        worker = client.k8s_worker.get(
            id="/api/v2/worker/k8shost/5", setup_log=True
        )

        self.assertEquals(
            worker.ipaddr,
            "10.1.0.186",
        )

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
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

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_set_storage_no_disks(self, mock_get, mock_post):
        client = get_client()

        with self.assertRaises(AssertionError) as c:
            client.k8s_worker.set_storage(worker_id="/api/v2/worker/k8shost/5")
        self.assertEqual(
            str(c.exception),
            "'ephemeral_disks' must contain at least one disk",
        )

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
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

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
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

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_set_storage_only_ephemeral_disks(self, mock_get, mock_post):
        client = get_client()

        _sample_ep_disks = ["/dev/nvme2n1", "/dev/nvme2n2"]
        client.k8s_worker.set_storage(
            worker_id="/api/v2/worker/k8shost/5",
            ephemeral_disks=_sample_ep_disks,
        )

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_cli(self, mock_get, mock_post):

        try:
            hpecp_cli = self.cli.CLI()
            hpecp_cli.k8sworker.set_storage(
                id="/api/v2/worker/k8shost/5",
                ephemeral_disks="abc,def",
                persistent_disks="ghi,jkl",
            )
        except Exception as e:
            self.fail("Unexpected exception: {}".format(e))


class TestCliCreate(BaseTestCase):
    def test_key_or_keycontent_provided(
        self,
    ):

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

    def test_key_and_keycontent_provided(
        self,
    ):

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

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("hpecp.k8s_worker")
    def test_with_only_ssh_key_content_provided(
        self, mock_post, mock_k8sworker
    ):

        """Test that the ssh key content provided by the 'ssh_key' parameter
        is passed to the library method 'create_with_ssh_key()'.
        """

        def mock_k8s_worker_get(*args, **kwargs):
            worker = WorkerK8s(
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
                    "_links": {"self": {"href": "/api/v2/worker/k8shost/5"}},
                }
            )
            return worker

        def mock_create_with_ssh_key(*args, **kwargs):
            return "/api/v2/worker/k8shost/5"

        def mock_get_client():
            client = ContainerPlatformClient(
                username="",
                password="",
                api_host="",
                api_port=9090,
                use_ssl=True,
                verify_ssl=True,
                warn_ssl=True,
            )
            client.session_id = "ABC"
            client.k8s_worker.get = mock_k8s_worker_get
            client.k8s_worker.create_with_ssh_key = mock_create_with_ssh_key
            return client

        # support debugging if this test fails
        with patch.dict("os.environ", {"LOG_LEVEL": "DEBUG"}):
            hpecp_cli = self.cli.CLI()

            # manually patch methods due to json serialization error
            # when using Mock or MagicMock
            base.get_client = mock_get_client

            hpecp_cli.k8sworker.create_with_ssh_key(
                ip="127.0.0.1",
                ssh_key="test_ssh_key",
            )

        stdout = self.out.getvalue().strip()

        self.assertEqual(stdout, "/api/v2/worker/k8shost/5")

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
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
                    ip="127.0.0.1",
                    ssh_key="test_ssh_key",
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

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("hpecp.k8s_worker")
    def test_with_only_ssh_key_content_provided_raises_conflict_exception(
        self, mock_post, mock_k8sworker
    ):

        with patch.object(
            K8sWorkerController,
            "create_with_ssh_key",
            side_effect=APIItemConflictException(
                message="APIItemConflictException.message",
                request_method="METHOD",
                request_url="URL",
            ),
        ):
            with self.assertRaises(SystemExit) as cm:
                hpecp_cli = self.cli.CLI()
                hpecp_cli.k8sworker.create_with_ssh_key(
                    ip="127.0.0.1",
                    ssh_key="test_ssh_key",
                )

        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_err = "APIItemConflictException.message"

        self.assertEqual(stdout, "")
        self.assertTrue(
            stderr.endswith(expected_err),
            "Expected: `{}`, Actual: `{}`".format(expected_err, stderr),
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
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
                    ip="127.0.0.1",
                    ssh_key="test_ssh_key",
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

    @patch(
        "requests.post", side_effect=BaseTestCase.httpPostHandlers
    )  # Login response
    def test_with_only_ssh_key_file_provided(self, mock_login_response):

        ssh_key_file = tempfile.NamedTemporaryFile(delete=True, mode="w")
        ssh_key_file.write("test_ssh_key_file_data")
        ssh_key_file.flush()

        def mock_k8s_worker_get(*args, **kwargs):
            worker = WorkerK8s(
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
                    "_links": {"self": {"href": "/api/v2/worker/k8shost/5"}},
                }
            )
            return worker

        def mock_create_with_ssh_key(*args, **kwargs):
            return "/api/v2/worker/k8shost/5"

        def mock_get_client():
            client = ContainerPlatformClient(
                username="",
                password="",
                api_host="",
                api_port=9090,
                use_ssl=True,
                verify_ssl=True,
                warn_ssl=True,
            )
            client.session_id = "ABC"
            client.k8s_worker.get = mock_k8s_worker_get
            client.k8s_worker.create_with_ssh_key = mock_create_with_ssh_key
            return client

        # support debugging if this test fails
        with patch.dict("os.environ", {"LOG_LEVEL": "DEBUG"}):
            hpecp_cli = self.cli.CLI()

            # manually patch methods due to json serialization error
            # when using Mock or MagicMock
            base.get_client = mock_get_client

            hpecp_cli.k8sworker.create_with_ssh_key(
                ip="127.0.0.1", ssh_key_file=ssh_key_file.name
            )

        stdout = self.out.getvalue().strip()

        self.assertEqual(stdout, "/api/v2/worker/k8shost/5")

        ssh_key_file.close()

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_ip_not_provided(self, mocked_requests_post):

        hpecp = self.cli.CLI()
        with self.assertRaises(SystemExit) as cm:
            hpecp.k8sworker.create_with_ssh_key(ssh_key="test data", ip=None)

        self.assertEqual(cm.exception.code, 1)

        actual_err = self.err.getvalue().strip()
        expected_err = "'ip' must be provided and must be a string"

        self.assertEqual(self.out.getvalue(), "", "stdout should be empty")

        self.assertTrue(
            actual_err.endswith(expected_err),
            "Actual stderr: `{}` Expected stderr: `{}`".format(
                actual_err, expected_err
            ),
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_ssh_key_not_a_string(self, mocked_requests_post):

        hpecp = self.cli.CLI()
        with self.assertRaises(SystemExit) as cm:
            hpecp.k8sworker.create_with_ssh_key(ssh_key=123, ip="127.0.0.1")

        self.assertEqual(cm.exception.code, 1)

        actual_err = self.err.getvalue().strip()
        expected_err = "'ssh_key_data' must be provided and must be a string"

        self.assertEqual(self.out.getvalue(), "", "stdout should be empty")

        self.assertTrue(
            actual_err.endswith(expected_err),
            "Actual stderr: `{}` Expected stderr: `{}`".format(
                actual_err, expected_err
            ),
        )


class TestCliStates(BaseTestCase):
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_states(self, mock_post):

        self.maxDiff = None

        hpecp = self.cli.CLI()
        hpecp.k8sworker.statuses()

        stdout = self.out.getvalue().strip()

        expected_stdout = (
            "['bundle', 'installing', 'installed', 'ready', "
            "'unlicensed', 'configuring', 'configured', 'error', "
            "'sysinfo', 'unconfiguring', 'deleting', "
            "'storage_pending', 'storage_configuring', "
            "'storage_error']"
        )

        self.assertEqual(stdout, expected_stdout)


class TestCliSetStorage(BaseTestCase):
    @patch("hpecp.k8s_worker")
    def test_wwithout_ephemeral_storage_prints_err(self, mock_k8sworker):

        with patch.object(
            K8sWorkerController,
            "set_storage",
            return_value=None,
        ):

            with self.assertRaises(SystemExit) as cm:
                try:
                    hpecp_cli = self.cli.CLI()
                    hpecp_cli.k8sworker.set_storage(
                        id="12345",
                        ephemeral_disks=None,
                        persistent_disks=None,
                    )
                except Exception as e:
                    self.fail("Unexpected exception: {}".format(e))

        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        exptected_stderr = "'ephemeral_disks' must be provided"

        self.assertEqual(stdout, "")
        self.assertTrue(
            stderr.endswith(exptected_stderr),
            "Expected: `{}` Actual: `{}`".format(exptected_stderr, stderr),
        )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    @patch("hpecp.k8s_worker")
    def test_with_exception(self, mock_post, mock_k8sworker):

        with patch.object(
            K8sWorkerController,
            "set_storage",
            side_effect=Exception("TEST_EXCEPTION"),
        ):

            with self.assertRaises(SystemExit) as cm:
                try:
                    hpecp_cli = self.cli.CLI()
                    hpecp_cli.k8sworker.set_storage(
                        id="12345",
                        ephemeral_disks="abc,def",
                        persistent_disks="ghi,jkl",
                    )
                except Exception as e:
                    self.fail("Unexpected exception: {}".format(e))

        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        exptected_stderr = (
            "Unknown error. To debug run with env var LOG_LEVEL=DEBUG"
        )

        self.assertEqual(stdout, "")
        self.assertTrue(
            stderr.endswith(exptected_stderr),
            "Expected: `{}` Actual: `{}`".format(exptected_stderr, stderr),
        )
