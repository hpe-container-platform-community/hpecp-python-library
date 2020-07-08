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

from unittest import TestCase

import requests
from mock import Mock, patch

from hpecp import (
    APIItemNotFoundException,
    ContainerPlatformClient,
)
from hpecp.gateway import GatewayController, GatewayStatus
from textwrap import dedent
import tempfile
import os
import sys
import six

from .base_test import BaseTestCase
from hpecp.exceptions import APIItemConflictException

if six.PY2:
    from io import BytesIO as StringIO
else:
    from io import StringIO


class MockResponse:
    def __init__(
        self,
        json_data,
        status_code,
        headers,
        raise_for_status_flag=False,
        raise_exception=False,
        text_data="",
    ):
        self.json_data = json_data
        self.text = text_data
        self.status_code = status_code
        self.raise_for_status_flag = raise_for_status_flag
        self.raise_exception = raise_exception
        self.headers = headers

    def raise_for_status(self):
        if self.raise_for_status_flag:
            self.text = "some error occurred"
            raise requests.exceptions.HTTPError()
        elif self.raise_exception:
            self.text = "some error occurred"
            raise Exception()
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


class TestGatewayGet(TestCase):

    # pylint: disable=no-method-argument
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/workers/99":
            return MockResponse(
                json_data={
                    "hacapable": True,
                    "propinfo": {
                        "bds_storage_apollo": "false",
                        "bds_network_publicinterface": "ens5",
                    },
                    "approved_worker_pubkey": [],
                    "schedule": False,
                    "ip": "10.1.0.37",
                    "proxy_nodes_hostname": (
                        "ec2-35-165-137-87.us-west-2.compute.amazonaws.com"
                    ),
                    "hostname": "ip-10-1-0-37.us-west-2.compute.internal",
                    "state": "installed",
                    "_links": {"self": {"href": "/api/v1/workers/99"}},
                    "purpose": "proxy",
                    "status_info": "",
                    "sysinfo": {
                        "network": [
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "7e:d0:19:00:a1:c0",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-6-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "52:c4:7b:93:f2:0a",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-2-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "b2:e6:2b:c5:7a:d4",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-0-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "UNKNOWN",
                                    "Carrier": "UNKNOWN",
                                    "HwAddr": "c6:b3:cd:1b:7d:44",
                                    "Speed": "UNKNOWN",
                                },
                                "name": "bds-flood",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "5a:16:20:0c:d7:f1",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-1-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "c6:bf:e3:af:82:2f",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-1-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "0e:d9:23:62:96:94",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-0-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "e2:86:7e:62:c0:3c",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-2-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "8e:92:dc:b9:b7:d7",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-6-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": False,
                                    "IpAddr": {"dynamic": "10.1.0.37/24"},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "02:72:98:8e:3b:86",
                                    "Speed": "UNKNOWN",
                                },
                                "name": "ens5",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "2a:4a:c9:c6:d0:28",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-4-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "7a:22:39:fc:11:7e",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-5-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "9a:2f:6c:e6:74:30",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-3-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "7e:ff:e4:5b:56:0d",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-7-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "4a:f7:7e:95:14:2d",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-7-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "36:5f:82:61:bf:5c",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-3-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "6e:86:7d:52:94:5d",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-5-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "e6:24:0f:54:99:a9",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-4-l",
                            },
                        ],
                        "keys": {
                            "reported_worker_public_key": (
                                "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDKonff"
                                "u4vtTSINNpBwvLd367941fhPyEuVfh7KrohdIUSVEh/p"
                                "X8FDAO9fi9pH979AzdDVWeUclTmktm63vQ39TVIJQ+rq"
                                "doZUhtH8rSYFoTFzxUQxONviNJJGTiYYMo4kJsLO1Hk/"
                                "b9Lz8sxUJWD+e5r2UTM5cDSYT3wBHUCDr/MXAxNC9FAg"
                                "kpuME5utC1dd1aHj2zgLUP61REjnhy1zVVJnbh/T/y3p"
                                "8Z5z0ubAQy7pYaMTuWgdVMH6kA/RWzOB2JRj8vFKYp9f"
                                "ysFe7L/nj+C2LkDr4dmMLNL9ffTvpnMOj5qPgAO8bay5"
                                "hAgVykUaRInLjuL7p5/nFATm9uI4A2a28m4HO9csywNX"
                                "pm5TBDWPDxW7Wh7Sdkx0xHwZenXXy/em+4Q4Fk4Oc6Yw"
                                "YcKOJVsst0qGeCFkhLjzvFHu2ceYf5Q1gg5FlBiX+LsW"
                                "ngjArsd0sdh+3piH/xFuHdubqHfOFpOlZsQsMX5V/LUA"
                                "71Wqv/cxMsoD5jybQOUS8o34JjkCZlavuJcIeU4hWlWE"
                                "liZU5SmppuNkHdosXup20/TyBgg0qYlzc+FKZ/8vlQSj"
                                "T5WgCNffPgXR94KPF1817RW1YSbR+1oiNg6FXgQrKM/1"
                                "DiqyQ5D8DjhZWgg33hJ7K/fKCL3qPyWCJEMQ64iLQ4Qt"
                                "SeU46l+aO490A89u6w== server\n"
                            )
                        },
                        "storage": [
                            {
                                "info": {
                                    "IsLogicalVolume": False,
                                    "IsDisk": False,
                                    "Name": "/dev/nvme0n1p1",
                                    "SizeBytes": "429495664128",
                                    "IsReadOnly": False,
                                    "ParentName": "/dev/nvme0n1",
                                    "IsRemovable": False,
                                    "IsRotational": False,
                                    "ParentDeviceType": "disk",
                                    "IsPartition": True,
                                    "DeviceType": "part",
                                    "HasFilesystem": True,
                                    "Mountpoint": "/",
                                },
                                "name": "/dev/nvme0n1p1",
                            }
                        ],
                        "swap": {"swap_total": 0},
                        "memory": {"mem_total": 65842458624},
                        "gp": {"gpu_count": 0},
                        "cp": {
                            "cpu_logical_cores": 16,
                            "cpu_count": 8,
                            "cpu_physical_cores": 8,
                            "cpu_sockets": 1,
                        },
                        "mountpoint": [],
                    },
                    "tags": [],
                },
                status_code=200,
                headers={},
            )
        if args[0] == "https://127.0.0.1:8080/api/v1/workers/100":
            return MockResponse(
                json_data={
                    "hacapable": True,
                    "propinfo": {
                        "bds_storage_apollo": "false",
                        "bds_network_publicinterface": "ens5",
                    },
                    "approved_worker_pubkey": [],
                    "schedule": False,
                    "ip": "10.1.0.37",
                    "proxy_nodes_hostname": (
                        "ec2-35-165-137-87.us-west-2.compute.amazonaws.com"
                    ),
                    "hostname": "ip-10-1-0-37.us-west-2.compute.internal",
                    "state": "installed",
                    "_links": {"self": {"href": "/api/v1/workers/99"}},
                    "purpose": "controller",
                    "status_info": "",
                    "sysinfo": {
                        "network": [
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "7e:d0:19:00:a1:c0",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-6-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "52:c4:7b:93:f2:0a",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-2-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "b2:e6:2b:c5:7a:d4",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-0-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "UNKNOWN",
                                    "Carrier": "UNKNOWN",
                                    "HwAddr": "c6:b3:cd:1b:7d:44",
                                    "Speed": "UNKNOWN",
                                },
                                "name": "bds-flood",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "5a:16:20:0c:d7:f1",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-1-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "c6:bf:e3:af:82:2f",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-1-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "0e:d9:23:62:96:94",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-0-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "e2:86:7e:62:c0:3c",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-2-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "8e:92:dc:b9:b7:d7",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-6-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": False,
                                    "IpAddr": {"dynamic": "10.1.0.37/24"},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "02:72:98:8e:3b:86",
                                    "Speed": "UNKNOWN",
                                },
                                "name": "ens5",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "2a:4a:c9:c6:d0:28",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-4-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "7a:22:39:fc:11:7e",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-5-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "9a:2f:6c:e6:74:30",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-3-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "7e:ff:e4:5b:56:0d",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-7-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "4a:f7:7e:95:14:2d",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-7-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "36:5f:82:61:bf:5c",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-3-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "6e:86:7d:52:94:5d",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-5-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "e6:24:0f:54:99:a9",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-4-l",
                            },
                        ],
                        "keys": {
                            "reported_worker_public_key": (
                                "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDKonff"
                                "u4vtTSINNpBwvLd367941fhPyEuVfh7KrohdIUSVEh/p"
                                "X8FDAO9fi9pH979AzdDVWeUclTmktm63vQ39TVIJQ+rq"
                                "oZUhtH8rSYFoTFzxUQxONviNJJGTiYYMo4kJsLO1Hk/b"
                                "9Lz8sxUJWD+e5r2UTM5cDSYT3wBHUCDr/MXAxNC9FAgk"
                                "puME5utC1dd1aHj2zgLUP61REjnhy1zVVJnbh/T/y3p8"
                                "Z5z0ubAQy7pYaMTuWgdVMH6kA/RWzOB2JRj8vFKYp9fy"
                                "sFe7L/nj+C2LkDr4dmMLNL9ffTvpnMOj5qPgAO8bay5h"
                                "AgVykUaRInLjuL7p5/nFATm9uI4A2a28m4HO9csywNXp"
                                "m5TBDWPDxW7Wh7Sdkx0xHwZenXXy/em+4Q4Fk4Oc6YwY"
                                "cKOJVsst0qGeCFkhLjzvFHu2ceYf5Q1gg5FlBiX+LsWn"
                                "gjArsd0sdh+3piH/xFuHdubqHfOFpOlZsQsMX5V/LUA7"
                                "1Wqv/cxMsoD5jybQOUS8o34JjkCZlavuJcIeU4hWlWEl"
                                "iZU5SmppuNkHdosXup20/TyBgg0qYlzc+FKZ/8vlQSjT"
                                "5WgCNffPgXR94KPF1817RW1YSbR+1oiNg6FXgQrKM/1D"
                                "iqyQ5D8DjhZWgg33hJ7K/fKCL3qPyWCJEMQ64iLQ4QtS"
                                "eU46l+aO490A89u6w== server\n"
                            )
                        },
                        "storage": [
                            {
                                "info": {
                                    "IsLogicalVolume": False,
                                    "IsDisk": False,
                                    "Name": "/dev/nvme0n1p1",
                                    "SizeBytes": "429495664128",
                                    "IsReadOnly": False,
                                    "ParentName": "/dev/nvme0n1",
                                    "IsRemovable": False,
                                    "IsRotational": False,
                                    "ParentDeviceType": "disk",
                                    "IsPartition": True,
                                    "DeviceType": "part",
                                    "HasFilesystem": True,
                                    "Mountpoint": "/",
                                },
                                "name": "/dev/nvme0n1p1",
                            }
                        ],
                        "swap": {"swap_total": 0},
                        "memory": {"mem_total": 65842458624},
                        "gp": {"gpu_count": 0},
                        "cp": {
                            "cpu_logical_cores": 16,
                            "cpu_count": 8,
                            "cpu_physical_cores": 8,
                            "cpu_sockets": 1,
                        },
                        "mountpoint": [],
                    },
                    "tags": [],
                },
                status_code=200,
                headers={},
            )
        raise RuntimeError("Unhandle GET request: " + args[0])

    def mocked_requests_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return session_mock_response()
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_gateway_assertions(self, mock_get, mock_post):

        with self.assertRaisesRegexp(
            AssertionError, "'id' must be provided and must be a str",
        ):
            get_client().gateway.get(123)

        # pylint: disable=anomalous-backslash-in-string
        with self.assertRaisesRegexp(
            AssertionError, "'id' does not start with '/api/v1/workers'"
        ):
            get_client().gateway.get("garbage")

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_get_gateway(self, mock_get, mock_post):

        gateway = get_client().gateway.get("/api/v1/workers/99")

        self.assertEqual(gateway.id, "/api/v1/workers/99")

        # TODO test other property accessors

        # /api/v1/workers/100 has "'purpose': 'controller'" so it
        #  isn't a gateway
        with self.assertRaisesRegexp(
            APIItemNotFoundException,
            "'gateway not found with id: /api/v1/workers/100'",
        ):
            get_client().gateway.get("/api/v1/workers/100")


class TestCreateGateway(TestCase):

    # pylint: disable=no-method-argument
    def mocked_requests_create_post(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/login":
            return session_mock_response()
        elif args[0] == "https://127.0.0.1:8080/api/v1/workers":
            return MockResponse(
                json_data={},
                status_code=200,
                headers={"Location": "/api/v2/workers/99"},
            )
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.post", side_effect=mocked_requests_create_post)
    def test_create_with_ssh_key_assertions(self, mock_post):

        with self.assertRaisesRegexp(
            AssertionError, "'ip' must be provided and must be a string"
        ):
            get_client().gateway.create_with_ssh_key(
                ip=123,
                proxy_node_hostname="my.host.name",
                ssh_key_data="pem encoded key data",
            )

        # TODO add more assertions

    @patch("requests.post", side_effect=mocked_requests_create_post)
    def test_create_with_ssh_key_returns_id(self, mock_post):

        # TODO
        pass


class TestWaitForGatewayStatus(BaseTestCase):

    # pylint: disable=no-method-argument
    def mocked_requests_get(*args, **kwargs):
        if args[0] == "https://127.0.0.1:8080/api/v1/workers/123":
            return MockResponse(
                json_data={
                    "hacapable": True,
                    "propinfo": {
                        "bds_storage_apollo": "false",
                        "bds_network_publicinterface": "ens5",
                    },
                    "approved_worker_pubkey": [],
                    "schedule": False,
                    "ip": "10.1.0.37",
                    "proxy_nodes_hostname": (
                        "ec2-35-165-137-87.us-west-2.compute.amazonaws.com"
                    ),
                    "hostname": "ip-10-1-0-37.us-west-2.compute.internal",
                    "state": "installed",
                    "_links": {"self": {"href": "/api/v1/workers/123"}},
                    "purpose": "proxy",
                    "status_info": "",
                    "sysinfo": {
                        "network": [
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "7e:d0:19:00:a1:c0",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-6-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "52:c4:7b:93:f2:0a",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-2-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "b2:e6:2b:c5:7a:d4",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-0-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "UNKNOWN",
                                    "Carrier": "UNKNOWN",
                                    "HwAddr": "c6:b3:cd:1b:7d:44",
                                    "Speed": "UNKNOWN",
                                },
                                "name": "bds-flood",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "5a:16:20:0c:d7:f1",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-1-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "c6:bf:e3:af:82:2f",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-1-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "0e:d9:23:62:96:94",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-0-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "e2:86:7e:62:c0:3c",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-2-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "8e:92:dc:b9:b7:d7",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-6-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": False,
                                    "IpAddr": {"dynamic": "10.1.0.37/24"},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "02:72:98:8e:3b:86",
                                    "Speed": "UNKNOWN",
                                },
                                "name": "ens5",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "2a:4a:c9:c6:d0:28",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-4-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "7a:22:39:fc:11:7e",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-5-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "9a:2f:6c:e6:74:30",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-3-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "7e:ff:e4:5b:56:0d",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-7-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "4a:f7:7e:95:14:2d",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-7-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "36:5f:82:61:bf:5c",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-3-r",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "6e:86:7d:52:94:5d",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-5-l",
                            },
                            {
                                "info": {
                                    "IsVirtual": True,
                                    "IpAddr": {},
                                    "Mt": 9001,
                                    "State": "up",
                                    "Carrier": True,
                                    "HwAddr": "e6:24:0f:54:99:a9",
                                    "Speed": "10000",
                                },
                                "name": "bds-flood-4-l",
                            },
                        ],
                        "keys": {
                            "reported_worker_public_key": (
                                "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDKonff"
                                "u4vtTSINNpBwvLd367941fhPyEuVfh7KrohdIUSVEh/p"
                                "X8FDAO9fi9pH979AzdDVWeUclTmktm63vQ39TVIJQ+rq"
                                "oZUhtH8rSYFoTFzxUQxONviNJJGTiYYMo4kJsLO1Hk/b"
                                "9Lz8sxUJWD+e5r2UTM5cDSYT3wBHUCDr/MXAxNC9FAgk"
                                "puME5utC1dd1aHj2zgLUP61REjnhy1zVVJnbh/T/y3p8"
                                "Z5z0ubAQy7pYaMTuWgdVMH6kA/RWzOB2JRj8vFKYp9fy"
                                "sFe7L/nj+C2LkDr4dmMLNL9ffTvpnMOj5qPgAO8bay5h"
                                "AgVykUaRInLjuL7p5/nFATm9uI4A2a28m4HO9csywNXp"
                                "m5TBDWPDxW7Wh7Sdkx0xHwZenXXy/em+4Q4Fk4Oc6YwY"
                                "cKOJVsst0qGeCFkhLjzvFHu2ceYf5Q1gg5FlBiX+LsWn"
                                "gjArsd0sdh+3piH/xFuHdubqHfOFpOlZsQsMX5V/LUA7"
                                "1Wqv/cxMsoD5jybQOUS8o34JjkCZlavuJcIeU4hWlWEl"
                                "iZU5SmppuNkHdosXup20/TyBgg0qYlzc+FKZ/8vlQSjT"
                                "5WgCNffPgXR94KPF1817RW1YSbR+1oiNg6FXgQrKM/1D"
                                "iqyQ5D8DjhZWgg33hJ7K/fKCL3qPyWCJEMQ64iLQ4QtS"
                                "eU46l+aO490A89u6w== server\n"
                            )
                        },
                        "storage": [
                            {
                                "info": {
                                    "IsLogicalVolume": False,
                                    "IsDisk": False,
                                    "Name": "/dev/nvme0n1p1",
                                    "SizeBytes": "429495664128",
                                    "IsReadOnly": False,
                                    "ParentName": "/dev/nvme0n1",
                                    "IsRemovable": False,
                                    "IsRotational": False,
                                    "ParentDeviceType": "disk",
                                    "IsPartition": True,
                                    "DeviceType": "part",
                                    "HasFilesystem": True,
                                    "Mountpoint": "/",
                                },
                                "name": "/dev/nvme0n1p1",
                            }
                        ],
                        "swap": {"swap_total": 0},
                        "memory": {"mem_total": 65842458624},
                        "gp": {"gpu_count": 0},
                        "cp": {
                            "cpu_logical_cores": 16,
                            "cpu_count": 8,
                            "cpu_physical_cores": 8,
                            "cpu_sockets": 1,
                        },
                        "mountpoint": [],
                    },
                    "tags": [],
                },
                status_code=200,
                headers={},
            )
        if args[0] == "https://127.0.0.1:8080/api/v1/workers/999":
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
        raise RuntimeError("Unhandle POST request: " + args[0])

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
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

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_wait_for_status_gateway(self, mock_get, mock_post):

        self.assertTrue(
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/123",
                timeout_secs=1,
                state=[GatewayStatus.installed],
            )
        )

        self.assertFalse(
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/123",
                timeout_secs=1,
                state=[GatewayStatus.deleting],
            )
        )

        self.assertTrue(
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/123",
                timeout_secs=1,
                state=[GatewayStatus.installed, GatewayStatus.deleting],
            )
        )

        self.assertFalse(
            get_client().gateway.wait_for_state(
                gateway_id="/api/v1/workers/123",
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

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_wait_for_status_gateway_cli(self, mock_get, mock_post):

        try:
            hpecp = self.cli.CLI()
            hpecp.gateway.wait_for_state(
                id="/api/v1/workers/123",
                timeout_secs=1,
                states=[GatewayStatus.installed.name],
            )
        except SystemExit:
            self.fail("Should not raise a SystemExit")

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_wait_for_status_gateway_cli_fail_to_reach_state(
        self, mock_get, mock_post
    ):

        with self.assertRaises(SystemExit) as cm:
            hpecp = self.cli.CLI()
            hpecp.gateway.wait_for_state(
                id="/api/v1/workers/123",
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

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
    def test_wait_for_status_gateway_cli_multiple_states(
        self, mock_get, mock_post
    ):

        try:
            hpecp = self.cli.CLI()
            hpecp.gateway.wait_for_state(
                id="/api/v1/workers/123",
                timeout_secs=1,
                states=[
                    GatewayStatus.installed.name,
                    GatewayStatus.deleting.name,
                ],
            )
        except SystemExit:
            self.fail("Should not raise a SystemExit")

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
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

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
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

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("requests.post", side_effect=mocked_requests_post)
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

        try:
            hpecp = self.cli.CLI()
            hpecp.gateway.wait_for_delete(
                id="/api/v1/workers/999", timeout_secs=1
            )
        except SystemExit:
            self.fail("Should not raise a SystemExit")

    @patch("requests.post", side_effect=mocked_requests_post)
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


class TestDeleteGateway(TestCase):
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
            return MockResponse(json_data={}, status_code=200, headers={},)
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

        # pylint: disable=anomalous-backslash-in-string
        with self.assertRaisesRegexp(
            AssertionError, "'id' does not start with '/api/v1/workers'"
        ):
            get_client().gateway.delete(id="garbage")

        with self.assertRaises(APIItemNotFoundException):
            get_client().gateway.delete(id="/api/v1/workers/999")

        get_client().gateway.delete(id="/api/v1/workers/123")


class TestCliCreate(BaseTestCase):
    def test_key_or_keycontent_provided(self,):

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

    def test_key_and_keycontent_provided(self,):

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
                message="MESSAGE", request_method="METHOD", request_url="URL",
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

        expected_err = "Gateway already exists."

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

        self.assertEqual(
            stdout,
            "/api/v1/workers/1",
            "stdout should be empty, but is `{}`".format(stdout),
        )

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
