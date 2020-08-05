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
        url="https://127.0.0.1:8080/api/v1/tenant/",
        response=MockResponse(
            json_data={
                "_embedded": {
                    "tenants": [
                        {
                            "status": "ready",
                            "tenant_type": "docker",
                            "features": {
                                "ml_project": False,
                                "kubernetes_access": False,
                            },
                            "persistent_supported": True,
                            "member_key_available": "all_admins",
                            "quota": {},
                            "cluster_isolation_supported": True,
                            "inusequota": {
                                "disk": 0,
                                "cores": 0,
                                "memory": 0,
                                "persistent": 0,
                                "gpus": 0,
                            },
                            "external_user_groups": [],
                            "gpu_usage_supported": True,
                            "_links": {"self": {"href": "/api/v1/tenant/1"}},
                            "filesystem_mount_supported": True,
                            "tenant_enforcements": [],
                            "label": {
                                "name": "Site Admin",
                                "description": (
                                    "Site Admin Tenant"
                                    " for BlueData clusters"
                                ),
                            },
                            "constraints_supported": False,
                            "tenant_storage_quota_supported": False,
                        },
                        {
                            "status": "ready",
                            "tenant_type": "docker",
                            "features": {
                                "ml_project": False,
                                "kubernetes_access": False,
                            },
                            "persistent_supported": True,
                            "member_key_available": "all_admins",
                            "quota": {},
                            "cluster_isolation_supported": True,
                            "inusequota": {
                                "disk": 0,
                                "cores": 0,
                                "memory": 0,
                                "persistent": 0,
                                "gpus": 0,
                            },
                            "external_user_groups": [],
                            "gpu_usage_supported": True,
                            "_links": {"self": {"href": "/api/v1/tenant/2"}},
                            "filesystem_mount_supported": True,
                            "tenant_enforcements": [],
                            "label": {
                                "name": "Demo Tenant",
                                "description": (
                                    "Demo Tenant for BlueData Clusters"
                                ),
                            },
                            "constraints_supported": True,
                            "tenant_storage_quota_supported": True,
                            "qos_multiplier": 1,
                        },
                    ]
                },
                "_links": {"self": {"href": "/api/v1/tenant"}},
            },
            status_code=200,
            headers={},
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/tenant/1",
        response=MockResponse(
            json_data={
                "status": "ready",
                "features": {"ml_project": False, "kubernetes_access": False},
                "persistent_supported": True,
                "member_key_available": "all_admins",
                "quota": {},
                "cluster_isolation_supported": True,
                "inusequota": {
                    "disk": 0,
                    "cores": 0,
                    "memory": 0,
                    "persistent": 0,
                    "gpus": 0,
                },
                "external_user_groups": [],
                "gpu_usage_supported": True,
                "_links": {"self": {"href": "/api/v1/tenant/1"}},
                "filesystem_mount_supported": True,
                "tenant_enforcements": [],
                "label": {
                    "name": "Site Admin",
                    "description": ("Site Admin Tenant for BlueData clusters"),
                },
                "constraints_supported": False,
                "tenant_storage_quota_supported": False,
            },
            status_code=200,
            headers={},
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/tenant/2",
        response=MockResponse(
            json_data={
                "status": "ready",
                "tenant_type": "docker",
                "features": {"ml_project": False, "kubernetes_access": False},
                "persistent_supported": True,
                "member_key_available": "all_admins",
                "quota": {},
                "cluster_isolation_supported": True,
                "inusequota": {
                    "disk": 0,
                    "cores": 0,
                    "memory": 0,
                    "persistent": 0,
                    "gpus": 0,
                },
                "external_user_groups": [],
                "gpu_usage_supported": True,
                "_links": {"self": {"href": "/api/v1/tenant/2"}},
                "filesystem_mount_supported": True,
                "tenant_enforcements": [],
                "label": {
                    "name": "Demo Tenant",
                    "description": "Demo Tenant for BlueData Clusters",
                },
                "constraints_supported": True,
                "tenant_storage_quota_supported": True,
                "qos_multiplier": 1,
            },
            status_code=200,
            headers={},
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/tenant/100",
        response=MockResponse(
            json_data={},
            status_code=404,
            headers={},
            raise_for_status_flag=True,
        ),
    )
