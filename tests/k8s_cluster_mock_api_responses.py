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

    # Response for cluster list all
    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v2/k8scluster",
        response=MockResponse(
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
                            "status_message": "really ready",
                            "api_endpoint_access": "api:1234",
                            "dashboard_endpoint_access": "dashboard:1234",
                            "admin_kube_config": "xyz==",
                            "dashboard_token": "abc==",
                            "persistent_storage": {"nimble_csi": False},
                        }
                    ]
                },
            },
            status_code=200,
            headers={},
        ),
    )

    # Response for a cluster that doesn't exist
    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v2/k8scluster/999",
        response=MockResponse(
            json_data={},
            status_code=404,
            raise_for_status_flag=True,
            headers={},
        ),
    )

    # Response for a cluster that doesn't exist
    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v2/k8scluster/999?setup_log=true",
        response=MockResponse(
            json_data={},
            status_code=404,
            raise_for_status_flag=True,
            headers={},
        ),
    )

    # Response for a cluster that DOES exist
    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v2/k8scluster/123",
        response=MockResponse(
            json_data={
                "_links": {"self": {"href": "/api/v2/k8scluster/123"}},
                "label": {"name": "def", "description": "my cluster"},
                "k8s_version": "1.17.0",
                "pod_network_range": "10.192.0.0/12",
                "service_network_range": "10.96.0.0/12",
                "pod_dns_domain": "cluster.local",
                "created_by_user_id": "/api/v1/user/5",
                "created_by_user_name": "admin",
                "created_time": 1588260014,
                "k8shosts_config": [
                    {"node": "/api/v2/worker/k8shost/4", "role": "worker"},
                    {"node": "/api/v2/worker/k8shost/5", "role": "master"},
                ],
                "status": "ready",
                "status_message": "really ready",
                "api_endpoint_access": "api:1234",
                "dashboard_endpoint_access": "test_dashboard_url",
                "admin_kube_config": "test_admin_kube_config",
                "dashboard_token": "YWJjCg==",
                "persistent_storage": {"nimble_csi": False},
            },
            status_code=200,
            headers={},
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v2/k8scluster/123?setup_log=true",
        response=MockResponse(
            json_data={
                "_links": {"self": {"href": "/api/v2/k8scluster/123"}},
                "label": {"name": "def", "description": "my cluster"},
                "k8s_version": "1.17.0",
                "pod_network_range": "10.192.0.0/12",
                "service_network_range": "10.96.0.0/12",
                "pod_dns_domain": "cluster.local",
                "created_by_user_id": "/api/v1/user/5",
                "created_by_user_name": "admin",
                "created_time": 1588260014,
                "k8shosts_config": [
                    {"node": "/api/v2/worker/k8shost/4", "role": "worker"},
                    {"node": "/api/v2/worker/k8shost/5", "role": "master"},
                ],
                "status": "ready",
                "status_message": "really ready",
                "api_endpoint_access": "api:1234",
                "dashboard_endpoint_access": "dashboard:1234",
                "admin_kube_config": "xyz==",
                "dashboard_token": "abc==",
                "persistent_storage": {"nimble_csi": False},
            },
            status_code=200,
            headers={},
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v2/k8smanifest",
        response=MockResponse(
            json_data={
                "_version": "1.0",
                "supported_versions": [
                    "1.14.10",
                    "1.15.7",
                    "1.16.4",
                    "1.17.0",
                    "1.17.1",
                    "1.18.0",
                ],
                "version_info": {
                    "1.14.10": {
                        "_version": "1.0",
                        "min_upgrade_version": "1.13.0",
                        "relnote_url": (
                            "https://v1-14.docs.kubernetes.io/docs/setup"
                            "/release/notes/"
                        ),
                        "hpecsi": "1.14",
                    },
                    "1.15.7": {
                        "_version": "1.0",
                        "min_upgrade_version": "1.14.0",
                        "relnote_url": (
                            "https://v1-15.docs.kubernetes.io/docs/setup"
                            "/release/notes/"
                        ),
                        "hpecsi": "1.15",
                    },
                    "1.16.4": {
                        "_version": "1.0",
                        "min_upgrade_version": "1.15.0",
                        "relnote_url": (
                            "https://v1-16.docs.kubernetes.io/docs/setup"
                            "/release/notes/"
                        ),
                        "hpecsi": "1.16",
                    },
                    "1.17.0": {
                        "_version": "1.0",
                        "min_upgrade_version": "1.16.0",
                        "relnote_url": (
                            "https://v1-17.docs.kubernetes.io/docs/setup"
                            "/release/notes/"
                        ),
                        "hpecsi": "1.17",
                    },
                    "1.17.1": {
                        "_version": "1.0",
                        "min_upgrade_version": "1.17.0",
                        "relnote_url": (
                            "https://v1-17.docs.kubernetes.io/docs/setup"
                            "/release/notes/"
                        ),
                        "hpecsi": "1.17",
                    },
                    "1.18.0": {
                        "_version": "1.0",
                        "min_upgrade_version": "1.17.0",
                        "relnote_url": (
                            "https://kubernetes.io/docs/setup"
                            "/release/notes/"
                        ),
                        "hpecsi": "1.18",
                    },
                },
            },
            status_code=200,
            headers={},
        ),
    )

    BaseTestCase.registerHttpPostHandler(
        url="https://127.0.0.1:8080/api/v2/k8scluster",
        response=MockResponse(
            json_data={},
            status_code=200,
            headers={"Location": "/api/v2/k8scluster/99"},
        ),
    )

    BaseTestCase.registerHttpDeleteHandler(
        url="https://127.0.0.1:8080/api/v2/k8scluster/999",
        response=MockResponse(
            json_data={},
            status_code=404,
            raise_for_status_flag=True,
            headers={},
        ),
    )

    BaseTestCase.registerHttpDeleteHandler(
        url="https://127.0.0.1:8080/api/v2/k8scluster/123",
        response=MockResponse(
            json_data={
                "_links": {"self": {"href": "/api/v2/k8scluster/123"}},
                "label": {"name": "def", "description": "my cluster"},
                "k8s_version": "1.17.0",
                "pod_network_range": "10.192.0.0/12",
                "service_network_range": "10.96.0.0/12",
                "pod_dns_domain": "cluster.local",
                "created_by_user_id": "/api/v1/user/5",
                "created_by_user_name": "admin",
                "created_time": 1588260014,
                "k8shosts_config": [
                    {"node": "/api/v2/worker/k8shost/4", "role": "worker"},
                    {"node": "/api/v2/worker/k8shost/5", "role": "master"},
                ],
                "status": "ready",
                "status_message": "really ready",
                "api_endpoint_access": "api:1234",
                "dashboard_endpoint_access": "dashboard:1234",
                "admin_kube_config": "xyz==",
                "dashboard_token": "abc==",
                "persistent_storage": {"nimble_csi": False},
            },
            status_code=200,
            headers={},
        ),
    )
