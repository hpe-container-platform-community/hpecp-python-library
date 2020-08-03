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


def mockApiGetSetup():
    mockApiGetWorkers()
    mockApiGetWorkers97()
    mockApiGetWorkers98()
    mockApiGetWorkers99()
    mockApiGetWorkers100()
    mockApiGetWorkers999()


def mockApiGetWorkers():
    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/workers",
        response=MockResponse(
            json_data={
                "_links": {"self": {"href": "/api/v1/workers"}},
                "_embedded": {
                    "workers": [
                        {
                            "_links": {"self": {"href": "/api/v1/workers/1"}},
                            "ip": "10.1.0.223",
                            "purpose": "primary",
                            "state": "installed",
                            "hostname": "ip-10-1-0-223.us-west-2.compute.internal",
                            "sysinfo": {
                                "network": [
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "96:7b:70:f0:80:65",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-6-r",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "9e:ee:3e:55:4f:5e",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-2-r",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "f6:40:25:22:e4:9e",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-0-r",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "UNKNOWN",
                                            "Carrier": "UNKNOWN",
                                            "HwAddr": "72:c9:23:3a:10:4f",
                                            "Speed": "UNKNOWN",
                                        },
                                        "name": "bds-flood",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "56:ee:25:7b:21:d2",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-1-r",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "fe:a0:8c:a1:48:62",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-1-l",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "26:cf:9e:07:d2:30",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-0-l",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "5e:b2:25:ac:0d:a2",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-2-l",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "86:df:9f:11:4a:26",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-6-l",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": False,
                                            "IpAddr": {
                                                "dynamic": "10.1.0.223/24"
                                            },
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "02:74:0e:2c:c8:b6",
                                            "Speed": "UNKNOWN",
                                        },
                                        "name": "ens5",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "7a:84:67:be:a7:65",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-4-r",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "ee:c1:00:ad:ca:f0",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-5-r",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "e6:16:cf:dc:e0:60",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-3-l",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "ee:6c:a1:4c:75:1f",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-7-r",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "0e:76:6b:67:68:d8",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-7-l",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "f6:c9:f5:d9:a0:af",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-3-r",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "b2:dc:68:f1:b1:a0",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-5-l",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "16:2b:7b:14:15:85",
                                            "Speed": "10000",
                                        },
                                        "name": "bds-flood-4-l",
                                    },
                                ],
                                "keys": {
                                    "reported_worker_public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDk5SHYy1gwjEtERZNoIDmjgbomLa8psuM5q7+a0LvD3NsPDuvkQ2E2e32QAV5gCHy+yKteADIVK9BxonlQPxe/ArMzbHQjsfFaD+ek0oCr2xCs91wVTrK0LV/kTWLhgaVHDSJAw5U/36dnedMmmarxaV7GtzFVE2uzlIUl1Dr3Zvc7rZCBgLgB3cysVVzfBA9V/L1COl05GTC8jkRErASFX/F/93WbifNyF2+9Nnnnle/RX1Nc/GXaypjSLzGWIXFiuoztUP+DT4k/20izmMqEAF40LNHKpq6bkcjMU8S21boHjo7CtugIkhjwxp+k7dW0ls+SnvKx+3gi9sIFsTZxK7tBYd1dhPzHpl+G57N9YeusUXM4KAi1RGHR7Y1utWFUObfQi0Eh80b3T19gzHVS6AA7MCSbCOzxnWjgVZCMsckCm1YRiTsJ2vx1tcDsoEkl0sqivsF884ahWDZK/UBbx5ZJajrg56Mg27avsGXRc74U1OGRL1smF80OdBBeZ987+cqSqtp7lYDyfARh5CimE62Lljs7INWSQOWMx6ve4gSs/j+dj2e9H7YHXZKR3JvYzuf0J05u5i0jz55Kg2scmHsPgJsg6nMfAImPHtOW+c19olAhT5F5pbCBl9bHcdDgWXFZjjX9uZJCyW0ppLMXgke2qJxjPonG4n1oD49K3Q== server\n"
                                },
                                "storage": [
                                    {
                                        "info": {
                                            "IsDisk": False,
                                            "Name": "/dev/mapper/VolBDSCStore-thinpool",
                                            "IsReadOnly": False,
                                            "IsRemovable": False,
                                            "IsRotational": False,
                                            "DeviceType": "lvm",
                                            "HasFilesystem": True,
                                            "IsLogicalVolume": True,
                                            "IsPartition": False,
                                            "ParentName": "/dev/nvme2n1p1",
                                            "ParentDeviceType": "part",
                                            "SizeBytes": "548682072064",
                                            "Mountpoint": "/var/lib/docker",
                                        },
                                        "name": "/dev/mapper/VolBDSCStore-thinpool",
                                    },
                                    {
                                        "info": {
                                            "IsDisk": False,
                                            "Name": "/dev/nvme0n1p1",
                                            "IsReadOnly": False,
                                            "IsRemovable": False,
                                            "IsRotational": False,
                                            "DeviceType": "part",
                                            "HasFilesystem": True,
                                            "IsLogicalVolume": False,
                                            "IsPartition": True,
                                            "ParentName": "/dev/nvme0n1",
                                            "ParentDeviceType": "disk",
                                            "SizeBytes": "429495664128",
                                            "Mountpoint": "/",
                                        },
                                        "name": "/dev/nvme0n1p1",
                                    },
                                    {
                                        "info": {
                                            "IsDisk": True,
                                            "Name": "/dev/nvme1n1",
                                            "IsReadOnly": False,
                                            "IsRemovable": False,
                                            "IsRotational": False,
                                            "DeviceType": "disk",
                                            "HasFilesystem": False,
                                            "IsLogicalVolume": False,
                                            "IsPartition": False,
                                            "ParentName": "",
                                            "ParentDeviceType": "",
                                            "SizeBytes": "549755813888",
                                            "Mountpoint": "",
                                        },
                                        "name": "/dev/nvme1n1",
                                    },
                                ],
                                "gpu": {"gpu_count": 0},
                                "swap": {"swap_total": 0},
                                "memory": {"mem_total": 66547093504},
                                "mountpoint": [],
                                "cpu": {
                                    "cpu_logical_cores": 16,
                                    "cpu_count": 8,
                                    "cpu_physical_cores": 8,
                                    "cpu_sockets": 1,
                                },
                            },
                            "approved_worker_pubkey": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDk5SHYy1gwjEtERZNoIDmjgbomLa8psuM5q7+a0LvD3NsPDuvkQ2E2e32QAV5gCHy+yKteADIVK9BxonlQPxe/ArMzbHQjsfFaD+ek0oCr2xCs91wVTrK0LV/kTWLhgaVHDSJAw5U/36dnedMmmarxaV7GtzFVE2uzlIUl1Dr3Zvc7rZCBgLgB3cysVVzfBA9V/L1COl05GTC8jkRErASFX/F/93WbifNyF2+9Nnnnle/RX1Nc/GXaypjSLzGWIXFiuoztUP+DT4k/20izmMqEAF40LNHKpq6bkcjMU8S21boHjo7CtugIkhjwxp+k7dW0ls+SnvKx+3gi9sIFsTZxK7tBYd1dhPzHpl+G57N9YeusUXM4KAi1RGHR7Y1utWFUObfQi0Eh80b3T19gzHVS6AA7MCSbCOzxnWjgVZCMsckCm1YRiTsJ2vx1tcDsoEkl0sqivsF884ahWDZK/UBbx5ZJajrg56Mg27avsGXRc74U1OGRL1smF80OdBBeZ987+cqSqtp7lYDyfARh5CimE62Lljs7INWSQOWMx6ve4gSs/j+dj2e9H7YHXZKR3JvYzuf0J05u5i0jz55Kg2scmHsPgJsg6nMfAImPHtOW+c19olAhT5F5pbCBl9bHcdDgWXFZjjX9uZJCyW0ppLMXgke2qJxjPonG4n1oD49K3Q== server\n",
                            "propinfo": {
                                "bds_storage_apollo": "false",
                                "bds_storage_thinpooldev": "/dev/mapper/VolBDSCStore-thinpool",
                                "bds_network_publicinterface": "ens5",
                            },
                            "status_info": "",
                            "schedule": True,
                            "hacapable": True,
                            "tags": [],
                            "hdfs_disks_configured": "/dev/nvme2n1",
                            "container_disks_configured": "/dev/nvme1n1",
                            "hdfs_commission": True,
                            "hdfs_commission_status": "Normal",
                        },
                        {
                            "_links": {"self": {"href": "/api/v1/workers/2"}},
                            "ip": "10.1.0.196",
                            "purpose": "proxy",
                            "state": "installed",
                            "hostname": "ip-10-1-0-196.us-west-2.compute.internal",
                            "sysinfo": {
                                "network": [
                                    {
                                        "info": {
                                            "IsVirtual": False,
                                            "IpAddr": {
                                                "dynamic": "10.1.0.196/24"
                                            },
                                            "Mtu": 9001,
                                            "State": "up",
                                            "Carrier": True,
                                            "HwAddr": "02:51:ae:fd:6f:a8",
                                            "Speed": "UNKNOWN",
                                        },
                                        "name": "ens5",
                                    },
                                    {
                                        "info": {
                                            "IsVirtual": True,
                                            "IpAddr": {},
                                            "Mtu": 1500,
                                            "State": "UNKNOWN",
                                            "Carrier": "UNKNOWN",
                                            "HwAddr": "e6:5a:3f:7b:9f:41",
                                            "Speed": "UNKNOWN",
                                        },
                                        "name": "bds-flood",
                                    },
                                ],
                                "keys": {
                                    "reported_worker_public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCymOWzCBMjejpFgvrIcX3xr2XAoUtl5QIVUKYiq2lBS0NPYAJhe4wkp0NGLs640MuacHDfsizfA4iJspRElk7aZ9S6dYv4EeKsKAPGi0STobrFYy4J+Nxc8quXrJhq0Psj4N2YE2Y2NoDZI35tvLeQMgTAtRYgPeSri+shBba/wyHZan4ftR/mdOu1oNJAfXXQ0DIoUmkSqxgxGA2OwVHEh4eGw5j6idkN3HmdC911+3d7KePKKbqdsbV1tRA1rMcvCL94AykmSA8oqdecn3e3QD7OBiEWS2V10AlcvU0YWkG1Bp0TTKtmoXsU0wMegoAvETKcxzf1n+Y/aZ6/ZxzHODayAQu6R5IWDDtgcsGT4V8KCAP1EEJ47fsFFBoc+M21jAKLJPDuHSAANJUY1Z6+/RL5x1U5FmaLnbiL7QI3a7WJRtqPO9xZglW5mroolsjtdWR/gs6daNk/7W7Fy5MuPKmOE1nf1RAfCUh2WYcCInuQ5jnoXoz+5XndCBuJHu3Cy/ZpAF2PtSoZ52aRMnKD9wIb6flqVnVNViU/mf4Bn3r0l03PJMBoEodXGvezSM1jaQnyv8MwXsDk3NTqRA+AltCPFEu7rChz5B/XHcX7SLZK9/zNmi7jmHI5Hj22kQNTHP9FXf6Awvm2+k0TTk7HpGfNurW1igV090Imi23FGw== server\n"
                                },
                                "storage": [
                                    {
                                        "info": {
                                            "IsDisk": False,
                                            "Name": "/dev/nvme0n1p1",
                                            "IsReadOnly": False,
                                            "IsRemovable": False,
                                            "IsRotational": False,
                                            "DeviceType": "part",
                                            "HasFilesystem": True,
                                            "IsLogicalVolume": False,
                                            "IsPartition": False,
                                            "ParentName": "/dev/nvme0n1",
                                            "ParentDeviceType": "disk",
                                            "SizeBytes": "429495664128",
                                            "Mountpoint": "/",
                                        },
                                        "name": "/dev/nvme0n1p1",
                                    }
                                ],
                                "gpu": {"gpu_count": 0},
                                "swap": {"swap_total": 0},
                                "memory": {"mem_total": 66547085312},
                                "mountpoint": [],
                                "cpu": {
                                    "cpu_logical_cores": 16,
                                    "cpu_count": 8,
                                    "cpu_physical_cores": 8,
                                    "cpu_sockets": 1,
                                },
                            },
                            "approved_worker_pubkey": [],
                            "propinfo": {
                                "bds_storage_apollo": "false",
                                "bds_network_publicinterface": "ens5",
                            },
                            "status_info": "",
                            "schedule": False,
                            "hacapable": True,
                            "tags": [],
                            "proxy_nodes_hostname": "ip-10-1-0-196.us-west-2.compute.internal",
                        },
                    ]
                },
            },
            status_code=200,
            headers={},
        ),
    )


# purpose=controller (not proxy)
def mockApiGetWorkers97():
    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/workers/97",
        response=MockResponse(
            json_data={
                "hacapable": True,
                "propinfo": {
                    "bds_storage_apollo": "false",
                    "bds_network_publicinterface": "ens5",
                },
                "approved_worker_pubkey": ["test pub key"],
                "schedule": False,
                "ip": "10.1.0.37",
                "proxy_nodes_hostname": "ec2-35-165-137-87.us-west-2.compute.amazonaws.com",
                "hostname": "ip-10-1-0-37.us-west-2.compute.internal",
                "state": "installed",
                "_links": {"self": {"href": "/api/v1/workers/97"}},
                "purpose": "controller",
                "status_info": "test status info",
                "sysinfo": "test sysinfo",
                "tags": ["test tags"],
            },
            status_code=200,
            headers={},
        ),
    )


# worker with minimum sysinfo for testing
def mockApiGetWorkers98():
    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/workers/98",
        response=MockResponse(
            json_data={
                "hacapable": True,
                "propinfo": {
                    "bds_storage_apollo": "false",
                    "bds_network_publicinterface": "ens5",
                },
                "approved_worker_pubkey": ["test pub key"],
                "schedule": False,
                "ip": "10.1.0.37",
                "proxy_nodes_hostname": "ec2-35-165-137-87.us-west-2.compute.amazonaws.com",
                "hostname": "ip-10-1-0-37.us-west-2.compute.internal",
                "state": "installed",
                "_links": {"self": {"href": "/api/v1/workers/98"}},
                "purpose": "proxy",
                "status_info": "test status info",
                "sysinfo": "test sysinfo",
                "tags": ["test tags"],
            },
            status_code=200,
            headers={},
        ),
    )


def mockApiGetWorkers99():
    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/workers/99",
        response=MockResponse(
            json_data={
                "hacapable": True,
                "propinfo": {
                    "bds_storage_apollo": "false",
                    "bds_network_publicinterface": "ens5",
                },
                "approved_worker_pubkey": ["test pub key"],
                "schedule": False,
                "ip": "10.1.0.37",
                "proxy_nodes_hostname": "ec2-35-165-137-87.us-west-2.compute.amazonaws.com",
                "hostname": "ip-10-1-0-37.us-west-2.compute.internal",
                "state": "installed",
                "_links": {"self": {"href": "/api/v1/workers/99"}},
                "purpose": "proxy",
                "status_info": "test status info",
                "sysinfo": {
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
                "tags": ["test tags"],
            },
            status_code=200,
            headers={},
        ),
    )


def mockApiGetWorkers100():
    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/workers/100",
        response=MockResponse(
            json_data={
                "hacapable": True,
                "propinfo": {
                    "bds_storage_apollo": "false",
                    "bds_network_publicinterface": "ens5",
                },
                "approved_worker_pubkey": ["test pub key"],
                "schedule": False,
                "ip": "10.1.0.37",
                "proxy_nodes_hostname": (
                    "ec2-35-165-137-87.us-west-2.compute.amazonaws.com"
                ),
                "hostname": "ip-10-1-0-37.us-west-2.compute.internal",
                "state": "installed",
                "_links": {"self": {"href": "/api/v1/workers/100"}},
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
        ),
    )


# worker that doesn't exist
def mockApiGetWorkers999():
    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/workers/999",
        response=MockResponse(
            json_data={},
            status_code=404,
            raise_for_status_flag=True,
            headers={},
        ),
    )


def mockApiPostSetup():

    BaseTestCase.registerHttpPostHandler(
        url="https://127.0.0.1:8080/api/v1/workers/",
        response=MockResponse(
            json_data={
                "hacapable": True,
                "propinfo": {
                    "bds_storage_apollo": "false",
                    "bds_network_publicinterface": "ens5",
                },
                "approved_worker_pubkey": ["test pub key"],
                "schedule": False,
                "ip": "10.1.0.37",
                "hostname": "ip-10-1-0-37.us-west-2.compute.internal",
                "state": "installed",
                "_links": {"self": {"href": "/api/v1/workers/99"}},
                "purpose": "proxy",
                "status_info": "test status info",
                "sysinfo": "test sysinfo",
                "tags": ["test tags"],
            },
            status_code=200,
            headers={"Location": "/api/v1/workers/123"},
        ),
    )
