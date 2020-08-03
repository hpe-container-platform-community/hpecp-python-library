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


from .base_test import BaseTestCase, MockResponse


def mockApiGetSetup():
    mockApiGetWorkers()


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


def mockApiGetWorkers99():
    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/workers/99",
        response=MockResponse(status_code=200, headers={},),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/workers/100",
        response=MockResponse(status_code=200, headers={},),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/workers/101",
        response=MockResponse(status_code=200, headers={},),
    )

    BaseTestCase.registerHttpGetHandler(
        response=MockResponse(status_code=200, headers={},),
    )


def mockApiPostSetup():

    BaseTestCase.registerHttpPostHandler(
        url="https://127.0.0.1:8080/api/v1/workers",
        response=MockResponse(
            status_code=200, headers={"Location": "/api/v1/workers/123"},
        ),
    )
