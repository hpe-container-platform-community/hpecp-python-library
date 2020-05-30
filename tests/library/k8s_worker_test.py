from unittest import TestCase
from mock import Mock, patch

import sys
import tempfile
import os
import json
import requests
from requests.exceptions import RequestException
from hpecp import ContainerPlatformClient
from hpecp.k8s_worker import WorkerK8sStatus


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


class TestWorkers(TestCase):
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v2/worker/k8shost/":
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
                                "hostname": "ip-10-1-0-238.eu-west-2.compute.internal",
                                "ipaddr": "10.1.0.238",
                                "setup_log": "/var/log/bluedata/install/k8shost_setup_10.1.0.238-2020-4-26-18-41-16",
                                "_links": {
                                    "self": {
                                        "href": "/api/v2/worker/k8shost/4"
                                    }
                                },
                                "sysinfo": {
                                    "network": [],
                                    "keys": {
                                        "reported_worker_public_key": "ssh-rsa ...== server\n"
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
                                "setup_log": "/var/log/bluedata/install/k8shost_setup_10.1.0.186-2020-4-26-18-49-10",
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
    def test_get_k8shosts(self, mock_get, mock_post):

        client = ContainerPlatformClient(
            username="admin",
            password="admin123",
            api_host="127.0.0.1",
            api_port=8080,
            use_ssl=True,
        )

        # Makes POST Request: https://127.0.0.1:8080/api/v1/login
        client.create_session()

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
