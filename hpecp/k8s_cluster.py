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

from __future__ import absolute_import

import re
from enum import Enum

from requests.structures import CaseInsensitiveDict

from .base_resource import AbstractResource, AbstractWaitableResourceController

try:
    basestring
except NameError:
    basestring = str


class K8sClusterStatus(Enum):
    """Bases: enum.Enum

    The statuses for a K8S Cluster

    **Note:**

    The integer values do not have a meaning outside of this library.
    The API uses a string identifier with the status name rather than an
    integer value.
    """

    ready = 1
    creating = 2
    updating = 3
    upgrading = 4
    deleting = 5
    error = 6
    warning = 7


class K8sCluster(AbstractResource):
    """Create an instance of K8sCluster from json data returned from the HPE
    Container Platform API.

    Users of this library are not expected to create an instance of this
    class.

    Parameters
    ----------
    json : str
        The json returned by the API representing a K8sCluster.

    Returns
    -------
    K8sCluster:
        An instance of K8sCluster
    """

    all_fields = [
        "id",
        "name",
        "description",
        "k8s_version",
        "addons",
        "created_by_user_id",
        "created_by_user_name",
        "created_time",
        "k8shosts_config",
        "admin_kube_config",
        "dashboard_token",
        "api_endpoint_access",
        "dashboard_endpoint_access",
        "cert_data",
        "status",
        "status_message",
        "_links",
    ]
    """All of the fields of a K8s Cluster objects that are returned by the HPE
    Container Platform API"""

    default_display_fields = [
        "id",
        "name",
        "description",
        "k8s_version",
        "status",
    ]

    @property
    def name(self):
        """@Field: from json['label']['name']"""
        return self.json["label"]["name"]

    @property
    def description(self):
        """@Field: from json['label']['description']"""
        return self.json["label"]["description"]

    @property
    def k8s_version(self):
        """@Field: from json['k8s_version']"""
        return self.json["k8s_version"]

    @property
    def addons(self):
        """@Field: from json['addons']"""
        if "addons" in self.json:
            return self.json["addons"]
        else:
            return ""

    @property
    def created_by_user_id(self):
        """@Field: from json['created_by_user_id']"""
        return self.json["created_by_user_id"]

    @property
    def created_by_user_name(self):
        """@Field: from json['created_by_user_name']"""
        return self.json["created_by_user_name"]

    @property
    def created_time(self):
        """@Field: from json['created_time']"""
        return self.json["created_time"]

    @property
    def k8shosts_config(self):
        """@Field: from json['k8shosts_config']"""
        return self.json["k8shosts_config"]

    @property
    def admin_kube_config(self):
        """@Field: from json['admin_kube_config']"""
        if "admin_kube_config" in self.json:
            return self.json["admin_kube_config"]
        else:
            return ""

    @property
    def dashboard_token(self):
        """@Field: from json['dashboard_token']"""
        if "dashboard_token" in self.json:
            return self.json["dashboard_token"]
        else:
            return ""

    @property
    def api_endpoint_access(self):
        """@Field: from json['api_endpoint_access']"""
        if "api_endpoint_access" in self.json:
            return self.json["api_endpoint_access"]
        else:
            return ""

    @property
    def dashboard_endpoint_access(self):
        """@Field: from json['dashboard_endpoint_access']"""
        if "dashboard_endpoint_access" in self.json:
            return self.json["dashboard_endpoint_access"]
        else:
            return ""

    @property
    def cert_data(self):
        """@Field: from json['cert_data'] or None if cert_data not available"""
        try:
            return self.json["cert_data"]
        except KeyError:
            return None

    @property
    def status(self):
        """@Field: from json['status']"""
        return self.json["status"]

    @property
    def status_message(self):
        """@Field: from json['status_message']"""
        if "status_message" in self.json:
            return self.json["status_message"]
        else:
            return ""


class K8sClusterHostConfig:
    """Object to represent a pair of `host node` and the `role` of the host
    - `master` or `worker`.
    """

    @classmethod
    def create_from_list(cls, noderole):
        """Factory method to create K8sClusterHostConfig from a list.

        Parameters
        ----------
        noderole: list
            the noderole must only have two values: [ node, role ]

        See Also
        --------
        See :py:meth:`K8sClusterHostConfig` for the allowed node and role
        values.
        """

        assert (
            len(noderole) == 2
        ), "'noderole' list must have two values [ node, role ]"
        return K8sClusterHostConfig(node=noderole[0], role=noderole[1])

    def __init__(self, node, role):
        assert isinstance(node, basestring), "'node' must be an string"
        assert re.match(
            r"\/api\/v2\/worker\/k8shost\/[0-9]+", node
        ), "'node' must have format '/api/v2/worker/k8shost/[0-9]+'"
        assert role in [
            "master",
            "worker",
        ], "'role' must one of ['master, worker']"

        self.node = node
        self.role = role

    def to_dict(self):
        """Returns a dict representation of the object.

        Returns
        -------
        dict

        Example
        -------
        >>> .to_dict()
        {
            'node': '/api/v2/worker/k8shost/12',
            'role': 'master'
        }
        """
        return {"node": self.node, "role": self.role}


class K8sClusterController(AbstractWaitableResourceController):
    """Class for interacting with K8S Clusters.

    An instance of this class is available in the
    client.ContainerPlatformClient with the attribute name
    :py:attr:`k8s_cluster <.client.ContainerPlatformClient.k8s_cluster>`.  The
    methods of this class can be invoked using `client.k8s_cluster.method()`.
    See the example below:

    Example
    -------
    >>> client = ContainerPlatformClient(...).create_session()
    >>> client.k8s_cluster.list()
    """

    base_resource_path = "/api/v2/k8scluster"

    resource_list_path = "k8sclusters"

    resource_class = K8sCluster

    status_class = K8sClusterStatus

    status_fieldname = "status"

    def create(
        self,
        name=None,
        description=None,
        k8s_version=None,
        pod_network_range="10.192.0.0/12",
        service_network_range="10.96.0.0/12",
        pod_dns_domain="cluster.local",
        persistent_storage_local=False,
        persistent_storage_nimble_csi=False,
        k8shosts_config=[],
        addons=[],
    ):
        """Send an API request to create a K8s Cluster.  The cluster creation
        will be asynchronous - use the :py:meth:`wait_for_status` method to
        wait for the cluster to be created.

        For the list of possible statuses see :py:class:`K8sClusterStatus`.

        Parameters
        ----------
        name: str
            Cluster name - required parameter.  Name must be at least 1
            character
        description: str
            Cluster description - defaults to empty string if not provided
        k8s_version: str
            Kubernetes version to configure. If not specified defaults to
            the latest version as supported by the rpms.
        pod_network_range: str
            Network range to be used for kubernetes pods. Defaults to
            `10.192.0.0/12`
        addons: list
            Addons - See :py:method:`get_available_addons`.
        service_network_range: str
            Network range to be used for kubernetes services that are
            exposed with Cluster IP. Defaults to `10.96.0.0/12`
        pod_dns_domain: str
            DNS Domain to be used for kubernetes pods. Defaults to
            `cluster.local`
        persistent_storage_local: str
            Enables local host storage to be available in the kubernetes
            cluster
        persistent_storage_nimble_csi: bool
            Set to True to installs the Nimble CSI plugin for Nimble
            storage to be available in the kubernetes cluster
        k8shosts_config: list[K8sClusterHostConfig]
            list of :py:class:`K8sClusterHostConfig` objects determining
            which hosts to add and their role (master or worker)

        Returns
        -------
        str
            K8s Cluster ID with the format: '/api/v2/k8scluster/[0-9]+'

        Raises
        ------
        APIException
        """

        assert (
            isinstance(name, basestring) and len(name) > 0
        ), "'name' must be provided and must be a string"
        assert description is None or isinstance(
            description, basestring
        ), "'description' if provided, must be a string"
        assert k8s_version is None or isinstance(
            k8s_version, basestring
        ), "'k8s_version' if provided, must be a string"
        assert isinstance(
            pod_network_range, basestring
        ), "'pod_network_range' must be a string"
        assert isinstance(
            service_network_range, basestring
        ), "'service_network_range' must be a string"
        assert isinstance(
            pod_dns_domain, basestring
        ), "'pod_dns_domain' must be a string"
        assert isinstance(
            persistent_storage_local, bool
        ), "'persistent_storage_local' must be True or False"
        assert isinstance(
            persistent_storage_nimble_csi, bool
        ), "'persistent_storage_nimble_csi' must be True or False"
        assert isinstance(
            k8shosts_config, list
        ), "'k8shosts_config' must be a list"
        assert (
            len(k8shosts_config) > 0
        ), "'k8shosts_config' must have at least one item"
        for i, conf in enumerate(k8shosts_config):
            assert isinstance(conf, K8sClusterHostConfig), (
                "'k8shosts_config' item '{}' is not of"
                " type K8sClusterHostConfig"
            ).format(i)
        assert isinstance(addons, list), "'addons' must be a list"

        data = {
            "label": {"name": name},
            "pod_network_range": pod_network_range,
            "service_network_range": service_network_range,
            "pod_dns_domain": pod_dns_domain,
            "addons": addons,
            "persistent_storage": {
                "local": persistent_storage_local,
                "nimble_csi": persistent_storage_nimble_csi,
            },
            "k8shosts_config": [c.to_dict() for c in k8shosts_config],
        }
        if description is not None:
            data["label"]["description"] = description
        if k8s_version is not None:
            data["k8s_version"] = k8s_version

        response = self.client._request(
            url="/api/v2/k8scluster",
            http_method="post",
            data=data,
            description="k8s_cluster/create",
        )
        return CaseInsensitiveDict(response.headers)["Location"]

    def get(self, id, params={}, setup_log=False):
        """Retrieve a K8s Cluster.

        Parameters
        ----------
        id: str
            The k8s cluster ID
        """
        if setup_log is True:
            params["setup_log"] = "true"

        return super(K8sClusterController, self).get(id=id, params=params)

    def k8smanifest(self):
        """Retrieve the k8smanifest.

        Returns
        -------
        json
            K8sManifest

        Raises
        ------
        APIException
        """
        response = self.client._request(
            url="/api/v2/k8smanifest",
            http_method="get",
            description="k8s_cluster/k8smanifest",
        )
        return response.json()

    def k8s_supported_versions(self):
        """Retrieve list of K8S Supported Versions.

        Returns
        -------
        list[str]
            List of K8s Supported Versions

        Raises
        ------
        APIException
        """
        return self.k8smanifest()["supported_versions"]

    def get_available_addons(self, id=None, k8s_version=None):
        """Retrieve list of K8S Supported Versions.

        Parameters
        ----------
        id: str
            The k8s cluster ID

        Returns
        -------
        list[str]
            List of available addons

        Raises
        ------
        APIException
        """
        assert (
            id is not None or k8s_version is not None
        ), "Either 'id' or 'k8s_version' parameter must be provided"
        assert (
            id is None or k8s_version is None
        ), "Either 'id' or 'k8s_version' parameter must be provided"

        if id:
            k8s_version = self.get(id).k8s_version

        return self.k8smanifest()["version_info"][k8s_version]["addons"]

    def add_addons(self, id, addons=[]):
        """Retrieve list of K8S Supported Versions.

        Parameters
        ----------
        id: str
            The k8s cluster ID
        addons: list
            The list of addons to add.

        Raises
        ------
        APIException
        """
        # TODO assert ID is provided and valid
        assert (
            isinstance(addons, list) and len(addons) > 0
        ), "'Addons' parameter must be a list and have at least one entry."

        current_addons = self.get(id).addons
        required_addons = current_addons + addons

        # de-duplicate
        required_addons = list(dict.fromkeys(required_addons))

        data = {
            "change_spec": {"addons": required_addons},
            "operation": "reconfigure",
            "reason": "",
        }

        self.client._request(
            url="{}/change_task".format(id),
            http_method="post",
            description="k8s_cluster/add_addons",
            data=data,
        )

    def upgrade_cluster(
        self, id, k8s_upgrade_version, worker_upgrade_percent=20
    ):
        """Upgrade a cluster.

        TODO

        Returns
        -------
        TODO

        Raises
        ------
        APIException
        """
        data = {
            "change_spec": {
                "k8s_upgrade": {
                    "worker_upgrade_percent": worker_upgrade_percent,
                    "k8s_upgrade_version": k8s_upgrade_version,
                }
            },
            "operation": "reconfigure",
            "reason": "Kubernetes upgrade",
        }

        response = self.client._request(
            url="{}/change_task".format(id),
            http_method="post",
            description="K8sClusterController/upgrade_cluster",
            data=data,
        )
        return response.json()

    def import_generic_cluster(
        self, name, description, pod_dns_domain, server_url, ca, bearer_token
    ):
        """Import a generic k8s cluster.

        TODO

        Returns
        -------
        TODO

        Raises
        ------
        APIException
        """
        data = {
            "label": {"name": name, "description": description},
            "pod_dns_domain": pod_dns_domain,
            "type": "generic",
            "sysadmin_data": {
                "server_url": server_url,
                "ca": ca,
                "bearer_token": bearer_token,
            },
        }

        response = self.client._request(
            url="/api/v2/k8scluster/import",
            http_method="post",
            description="K8sClusterController/import_generic_cluster",
            data=data,
        )
        return response.json()
