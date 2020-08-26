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

import tempfile

from mock import patch

from hpecp import APIItemNotFoundException
from hpecp.exceptions import APIItemConflictException
from hpecp.gateway import GatewayController, GatewayStatus

from .base import BaseTestCase, MockResponse, get_client
from .gateway_mock_api_responses import mockApiGetSetup, mockApiPostSetup


def session_mock_response():
    return MockResponse(
        json_data={},
        status_code=200,
        headers={
            "location": "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
        },
    )


class TestGatewayList(BaseTestCase):
    def setUp(self):
        mockApiGetSetup()
        # mockApiPostSetup()
        super(TestGatewayList, self).setUp()

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_list(self, mock_get, mock_post):

        # calls POST https://127.0.0.1:8080/api/v1/login
        # calls GET https://127.0.0.1:8080/api/v1/workers

        try:
            get_client().gateway.list()
        except Exception as e:
            # Unexpected exception
            self.fail(e)


class TestGatewayGet(BaseTestCase):
    def setUp(self):
        mockApiGetSetup()
        mockApiPostSetup()
        super(TestGatewayGet, self).setUp()

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_gateway_assertions(self, mock_get, mock_post):

        with self.assertRaisesRegexp(
            AssertionError,
            "'id' must be provided and must be a str",
        ):
            get_client().gateway.get(123)

        with self.assertRaisesRegexp(
            AssertionError, "'id' does not start with '/api/v1/workers'"
        ):
            get_client().gateway.get("garbage")

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_gateway(self, mock_get, mock_post):

        gateway = get_client().gateway.get("/api/v1/workers/99")

        self.assertEqual(gateway.id, "/api/v1/workers/99")
        self.assertEqual(gateway.hacapable, True)
        self.assertEqual(
            gateway.propinfo,
            {
                "bds_network_publicinterface": "ens5",
                "bds_storage_apollo": "false",
            },
        )
        self.assertEqual(gateway.approved_worker_pubkey, ["test pub key"])
        self.assertEqual(gateway.schedule, False)
        self.assertEqual(gateway.ip, "10.1.0.37")
        self.assertEqual(
            gateway.proxy_nodes_hostname,
            "ec2-35-165-137-87.us-west-2.compute.amazonaws.com",
        )
        self.assertEqual(
            gateway.hostname, "ip-10-1-0-37.us-west-2.compute.internal"
        )
        self.assertEqual(gateway.purpose, "proxy")
        self.assertEqual(gateway.status_info, "test status info")
        self.assertEqual(gateway.tags, ["test tags"])

        # /api/v1/workers/97 has "'purpose': 'controller'" so it
        #  isn't a gateway
        with self.assertRaisesRegexp(
            APIItemNotFoundException,
            "'gateway not found with id: /api/v1/workers/97'",
        ):
            get_client().gateway.get("/api/v1/workers/97")

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_gateway_sysinfo(self, mock_get, mock_post):

        gateway = get_client().gateway.get("/api/v1/workers/98")

        self.assertEqual(gateway.sysinfo, "test sysinfo")
        self.assertEqual(
            gateway.proxy_nodes_hostname,
            "ec2-35-165-137-87.us-west-2.compute.amazonaws.com",
        )


class TestCreateGateway(BaseTestCase):
    def setUp(self):
        mockApiGetSetup()
        mockApiPostSetup()
        super(TestCreateGateway, self).setUp()

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_create_with_ssh_key_assertions(self, mock_post):

        with self.assertRaisesRegexp(
            AssertionError, "'ip' must be provided and must be a string"
        ):
            get_client().gateway.create_with_ssh_key(
                ip=123,
                proxy_node_hostname="my.host.name",
                ssh_key_data="pem encoded key data",
            )

        with self.assertRaisesRegexp(
            AssertionError,
            "'proxy_node_hostname' must be provided and must be a string",
        ):
            get_client().gateway.create_with_ssh_key(
                ip="127.0.0.1",
                proxy_node_hostname=1234,
                ssh_key_data="pem encoded key data",
            )

        with self.assertRaisesRegexp(
            AssertionError,
            "'ssh_key_data' must be provided and must be a string",
        ):
            get_client().gateway.create_with_ssh_key(
                ip="127.0.0.1",
                proxy_node_hostname="abc",
                ssh_key_data=1234,
            )

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_create_with_ssh_key_returns_id(self, mock_post):

        get_client().gateway.create_with_ssh_key(
            ip="127.0.0.1",
            proxy_node_hostname="my.host.name",
            ssh_key_data="pem encoded key data",
        )


class TestWaitForGatewayStatus(BaseTestCase):
    def setUp(self):
        mockApiGetSetup()
        mockApiPostSetup()
        super(TestWaitForGatewayStatus, self).setUp()

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_wait_for_status_gateway_assertions(self, mock_get, mock_post):

        # FIXME speed these tests up

        with self.assertRaisesRegexp(
            AssertionError, "'id' must be provided and must be a str"
        ):
            get_client().gateway.wait_for_state(
                gateway_id=1, timeout_secs=1, state=[GatewayStatus.ready]
            )

        # pylint: disable=anomalous-backslash-in-string
        with self.assertRaisesRegexp(
            AssertionError, "'id' does not start with '/api/v1/workers'"
        ):
            get_client().gateway.wait_for_state(
                gateway_id="garbage",
                timeout_secs=1,
                state=[GatewayStatus.ready],
            )

        with self.assertRaisesRegexp(
            AssertionError, "'timeout_secs' must be an int"
        ):
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/123",
                timeout_secs="blah",
                state=[GatewayStatus.ready],
            )

        with self.assertRaisesRegexp(
            AssertionError, "'timeout_secs' must be >= 0"
        ):
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/123",
                timeout_secs=-1,
                state=[GatewayStatus.ready],
            )

        with self.assertRaisesRegexp(
            AssertionError,
            "'status' item '0' is not of type <enum 'GatewayStatus'>",
        ):
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/123", timeout_secs=1, state=["abc"]
            )

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_wait_for_status_gateway(self, mock_get, mock_post):

        self.assertTrue(
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/98",
                timeout_secs=1,
                state=[GatewayStatus.installed],
            )
        )

        self.assertFalse(
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/98",
                timeout_secs=1,
                state=[GatewayStatus.deleting],
            )
        )

        self.assertTrue(
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/98",
                timeout_secs=1,
                state=[GatewayStatus.installed, GatewayStatus.deleting],
            )
        )

        self.assertFalse(
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/98",
                timeout_secs=1,
                state=[GatewayStatus.error, GatewayStatus.deleting],
            )
        )

        # Get the status of a Cluster ID that doesn't exist
        with self.assertRaises(APIItemNotFoundException):
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/999",
                timeout_secs=1,
                state=[GatewayStatus.installed],
            )

        # Get the status of a Cluster ID that doesn't
        # exist - without providing a status
        self.assertTrue(
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/999", timeout_secs=1, state=[]
            )
        )

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_wait_for_status_gateway_cli(self, mock_get, mock_post):

        hpecp = self.cli.CLI()
        hpecp.gateway.wait_for_state(
            id="/api/v1/workers/98",
            timeout_secs=1,
            states=[GatewayStatus.installed.name],
        )

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_wait_for_status_gateway_cli_fail_to_reach_state(
        self, mock_get, mock_post
    ):

        with self.assertRaises(SystemExit) as cm:
            hpecp = self.cli.CLI()
            hpecp.gateway.wait_for_state(
                id="/api/v1/workers/98",
                timeout_secs=1,
                states=[GatewayStatus.deleting.name],
            )
        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = ""  # we don't want error output going to stdout
        expected_stderr = "Failed to reach state(s) ['deleting'] in 1s"

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error (issues 93)
        self.assertTrue(stderr.endswith(expected_stderr))

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_wait_for_status_gateway_cli_multiple_states(
        self, mock_get, mock_post
    ):

        hpecp = self.cli.CLI()
        hpecp.gateway.wait_for_state(
            id="/api/v1/workers/98",
            timeout_secs=1,
            states=[
                GatewayStatus.installed.name,
                GatewayStatus.deleting.name,
            ],
        )

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_wait_for_status_gateway_cli_fail_to_reach_state_with_multiple_states(
        self, mock_get, mock_post
    ):

        with self.assertRaises(SystemExit) as cm:
            hpecp = self.cli.CLI()
            hpecp.gateway.wait_for_state(
                id="/api/v1/workers/123",
                timeout_secs=1,
                states=[GatewayStatus.error.name, GatewayStatus.deleting.name],
            )
        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = ""  # we don't want error output going to stdout
        expected_stderr = (
            "Failed to reach state(s) ['error', 'deleting'] in 1s"
        )

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error (issues 93)
        self.assertTrue(stderr.endswith(expected_stderr))

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_wait_for_status_gateway_cli_gateway_id_does_not_exist(
        self, mock_get, mock_post
    ):

        # Get the status of a ID that doesn't exist
        with self.assertRaises(SystemExit) as cm:
            hpecp = self.cli.CLI()
            hpecp.gateway.wait_for_state(
                id="/api/v1/workers/999",
                timeout_secs=1,
                states=[GatewayStatus.installed.name],
            )
        self.assertEqual(cm.exception.code, 1)

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_wait_for_status_gateway_cli_gateway_id_does_not_exist_and_no_status(
        self, mock_get, mock_post
    ):

        # Get the status of a Cluster ID that doesn't
        # exist - without providing a status
        try:
            hpecp = self.cli.CLI()
            hpecp.gateway.wait_for_state(
                id="/api/v1/workers/999", timeout_secs=1, states=[]
            )
        except SystemExit:
            self.fail("Should not raise a SystemExit")

    @patch("requests.get", side_effect=BaseTestCase.httpGetHandlers)
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_wait_for_delete_gateway_cli_gateway_id_does_not_exist_and_no_status(
        self, mock_get, mock_post
    ):

        try:
            hpecp = self.cli.CLI()
            hpecp.gateway.wait_for_delete(
                id="/api/v1/workers/999", timeout_secs=1
            )
        except SystemExit:
            self.fail("Should not raise a SystemExit")

    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_get_states(self, mock_post):

        # TODO move me - I don't really belong in the
        #      wait_for_state test cases

        hpecp = self.cli.CLI()
        hpecp.gateway.states()

        stdout = self.out.getvalue().strip()

        expected_stdout = (
            "['bundle', 'installing', 'installed', 'ready', "
            "'unlicensed', 'configuring', 'configured', 'error', "
            "'sysinfo', 'unconfiguring', 'deleting', "
            "'storage_pending', 'storage_configuring', "
            "'storage_error', 'decommission_in_progress', "
            "'delete_in_progress']"
        )

        self.assertEqual(stdout, expected_stdout)


class TestDeleteGateway(BaseTestCase):
    # pylint: disable=no-method-argument
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/workers/123":
            return MockResponse(
                json_data={
                    "_links": {"self": {"href": "/api/v1/workers/123"}},
                    "purpose": "proxy",
                },
                status_code=200,
                headers={},
            )
        if args[0] == "https://127.0.0.1:8080/api/v1/workers/999":
            return MockResponse(
                text_data="Not found.",
                json_data={},
                status_code=404,
                raise_for_status_flag=True,
                headers={},
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    # pylint: disable=no-method-argument
    def mocked_requests_delete(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/workers/999":
            return MockResponse(
                text_data="Not found.",
                json_data={},
                status_code=404,
                raise_for_status_flag=True,
                headers={},
            )
        if args[0] == "https://127.0.0.1:8080/api/v1/workers/123":
            return MockResponse(
                json_data={},
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
                    "location": (
                        "/api/v1/session/df1bfacb-xxxx-xxxx-xxxx-c8f57d8f3c71"
                    )
                },
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    # delete() does a get() request to check the worker has 'purpose':'proxy'
    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.delete", side_effect=mocked_requests_delete)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_delete_gateway(self, mock_get, mock_post, mock_delete):

        with self.assertRaisesRegexp(
            AssertionError, "'id' does not start with '/api/v1/workers'"
        ):
            get_client().gateway.delete(id="garbage")

        with self.assertRaises(APIItemNotFoundException):
            get_client().gateway.delete(id="/api/v1/workers/999")

        get_client().gateway.delete(id="/api/v1/workers/123")


class TestCliCreate(BaseTestCase):
    def test_key_or_keycontent_provided(
        self,
    ):

        hpecp = self.cli.CLI()
        with self.assertRaises(SystemExit) as cm:
            hpecp.gateway.create_with_ssh_key(
                ip="127.0.0.1", proxy_node_hostname="somehost"
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

    def test_key_and_keycontent_provided(
        self,
    ):

        hpecp = self.cli.CLI()
        with self.assertRaises(SystemExit) as cm:
            hpecp.gateway.create_with_ssh_key(
                ip="127.0.0.1",
                proxy_node_hostname="somehost",
                ssh_key="foobar",
                ssh_key_file="foobar",
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
    @patch("hpecp.gateway")
    def test_with_only_ssh_key_content_provided(self, mock_post, mock_gateway):

        """Test that the ssh key content provided by the 'ssh_key' parameter
        is passed to the library method 'create_with_ssh_key()'.
        """

        with patch.object(
            GatewayController,
            "create_with_ssh_key",
            return_value="/api/v1/workers/1",
        ) as mock_create_with_ssh_key:
            try:
                hpecp = self.cli.CLI()
                hpecp.gateway.create_with_ssh_key(
                    ip="127.0.0.1",
                    proxy_node_hostname="somehost",
                    ssh_key="test_ssh_key",
                )
            except Exception:
                self.fail("Unexpected exception.")

        mock_create_with_ssh_key.assert_called_once_with(
            ip="127.0.0.1",
            proxy_node_hostname="somehost",
            ssh_key_data="test_ssh_key",
            tags=[],
        )

        stdout = self.out.getvalue().strip()

        self.assertEqual(stdout, "/api/v1/workers/1")

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("hpecp.gateway")
    def test_with_only_ssh_key_content_provided_raises_assertion_error(
        self, mock_post, mock_gateway
    ):

        with patch.object(
            GatewayController,
            "create_with_ssh_key",
            side_effect=AssertionError("TEST_ASSERTION"),
        ):
            with self.assertRaises(SystemExit) as cm:
                hpecp = self.cli.CLI()
                hpecp.gateway.create_with_ssh_key(
                    ip="127.0.0.1",
                    proxy_node_hostname="somehost",
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

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("hpecp.gateway")
    def test_with_only_ssh_key_content_provided_raises_conflict_exception(
        self, mock_post, mock_gateway
    ):

        with patch.object(
            GatewayController,
            "create_with_ssh_key",
            side_effect=APIItemConflictException(
                message="APIItemConflictException.message",
                request_method="METHOD",
                request_url="URL",
            ),
        ):
            with self.assertRaises(SystemExit) as cm:
                hpecp = self.cli.CLI()
                hpecp.gateway.create_with_ssh_key(
                    ip="127.0.0.1",
                    proxy_node_hostname="somehost",
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

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("hpecp.gateway")
    def test_with_only_ssh_key_content_provided_raises_general_exception(
        self, mock_post, mock_gateway
    ):

        with patch.object(
            GatewayController,
            "create_with_ssh_key",
            side_effect=Exception("TEST_EXCEPTION"),
        ):
            with self.assertRaises(SystemExit) as cm:
                hpecp = self.cli.CLI()
                hpecp.gateway.create_with_ssh_key(
                    ip="127.0.0.1",
                    proxy_node_hostname="somehost",
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

    @patch("requests.post", side_effect=mocked_requests_post)
    @patch("hpecp.gateway")
    def test_with_only_ssh_key_file_provided(self, mock_post, mock_gateway):

        ssh_key_file = tempfile.NamedTemporaryFile(delete=True, mode="w")
        ssh_key_file.write("test_ssh_key_file_data")
        ssh_key_file.flush()

        with patch.object(
            GatewayController,
            "create_with_ssh_key",
            return_value="/api/v1/workers/1",
        ) as mock_create_with_ssh_key:
            try:
                hpecp = self.cli.CLI()
                hpecp.gateway.create_with_ssh_key(
                    ip="127.0.0.1",
                    proxy_node_hostname="somehost",
                    ssh_key_file=ssh_key_file.name,
                )
            except Exception as e:
                self.fail("Unexpected exception. {}".format(e))

        mock_create_with_ssh_key.assert_called_once_with(
            ip="127.0.0.1",
            proxy_node_hostname="somehost",
            ssh_key_data="test_ssh_key_file_data",
            tags=[],
        )

        stdout = self.out.getvalue().strip()

        self.assertEqual(stdout, "/api/v1/workers/1")

        ssh_key_file.close()


class TestCliDelete(BaseTestCase):
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
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_post)
    # @patch("requests.del", side_effect=mocked_requests_delete)
    def test_delete_with_unknown_exception(self, mock_post):
        @patch("hpecp.base_resource.AbstractController")
        def delete(self, id):
            raise Exception()

        with self.assertRaises(SystemExit) as cm:
            hpecp = self.cli.CLI()
            hpecp.gateway.delete("/api/v1/workers/1")

        self.assertEqual(cm.exception.code, 1)

        stdout = self.out.getvalue().strip()
        stderr = self.err.getvalue().strip()

        expected_stdout = ""  # we don't want error output going to stdout
        expected_stderr = (
            "Unknown error. To debug run with env var LOG_LEVEL=DEBUG"
        )

        self.assertEqual(stdout, expected_stdout)

        # coverage seems to populate standard error (issues 93)
        self.assertTrue(stderr.endswith(expected_stderr))
