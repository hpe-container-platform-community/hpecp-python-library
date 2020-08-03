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


from .base import BaseTestCase, MockResponse


def mockApiSetup():

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v2/worker/k8shost",
        response=MockResponse(
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
                                "self": {"href": "/api/v2/worker/k8shost/4"}
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
                                "self": {"href": "/api/v2/worker/k8shost/5"}
                            },
                        },
                    ]
                }
            },
            status_code=200,
            headers={},
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v2/worker/k8shost/5",
        response=MockResponse(
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
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v2/worker/k8shost/5?setup_log=true",
        response=MockResponse(
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
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v2/worker/k8shost/8",
        response=MockResponse(
            json_data={},
            status_code=404,
            raise_for_status_flag=True,
            headers={},
        ),
    )

    BaseTestCase.registerHttpPostHandler(
        url="https://127.0.0.1:8080/api/v2/worker/k8shost/5",
        response=MockResponse(json_data={}, status_code=204, headers={}),
    )

    BaseTestCase.registerHttpPostHandler(
        url="https://127.0.0.1:8080/api/v2/worker/k8shost/",
        response=MockResponse(
            json_data={},
            status_code=201,
            headers={"location": "/new/cluster/id"},
        ),
    )
