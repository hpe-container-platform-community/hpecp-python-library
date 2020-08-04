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

from enum import Enum

from requests.structures import CaseInsensitiveDict

from .base_resource import AbstractResource, AbstractWaitableResourceController

try:
    basestring
except NameError:
    basestring = str


class WorkerK8sStatus(Enum):
    bundle = 1
    installing = 2
    installed = 3
    ready = 4
    unlicensed = 5
    configuring = 6
    configured = 7
    error = 8
    sysinfo = 9
    unconfiguring = 10
    deleting = 11
    storage_pending = 12
    storage_configuring = 13
    storage_error = 14


class WorkerK8s(AbstractResource):

    all_fields = [
        "id",
        "status",
        "hostname",
        "ipaddr",
        "href",
        "_links",
    ]
    """All of the fields of a K8s Cluster objects that are returned by the HPE
    Container Platform API"""

    default_display_fields = [
        "id",
        "status",
        "hostname",
        "ipaddr",
    ]

    @property
    def worker_id(self):
        return int(self.json["_links"]["self"]["href"].split("/")[-1])

    @property
    def status(self):
        return self.json["status"]

    @property
    def hostname(self):
        return self.json["hostname"]

    @property
    def ipaddr(self):
        return self.json["ipaddr"]

    @property
    def href(self):
        return self.json["_links"]["self"]["href"]


class K8sWorkerController(AbstractWaitableResourceController):

    base_resource_path = "/api/v2/worker/k8shost"

    resource_list_path = "k8shosts"

    resource_class = WorkerK8s

    status_class = WorkerK8sStatus

    status_fieldname = "status"

    # TODO implement me!
    # def create_with_ssh_password(self, username, password):
    #     """Not Implemented yet"""
    #     raise NotImplementedError()

    def create_with_ssh_key(self, ip, ssh_key_data, tags=[]):
        """Create a gateway instance using SSH key credentials to access the host.

        Parameters
        ----------
        ip: str
            The IP address of the proxy host.  Used for internal
            communication.
        ssh_key_data: str
            The ssh key data as a string.
        tags: list
            Tags to use, e.g. "{ 'tag1': 'foo', 'tag2', 'bar' }".

        Returns
        -------
        string
            Worker ID
        """

        assert isinstance(
            ip, basestring
        ), "'ip' must be provided and must be a string"
        assert isinstance(
            ssh_key_data, basestring
        ), "'ssh_key_data' must be provided and must be a string"

        data = {
            "ipaddr": ip,
            "credentials": {
                "type": "ssh_key_access",
                "ssh_key_data": ssh_key_data,
            },
            "tags": tags,
        }

        response = self.client._request(
            url="/api/v2/worker/k8shost/",
            http_method="post",
            data=data,
            description="K8sWorkerController/create_with_ssh_key",
        )
        return CaseInsensitiveDict(response.headers)["location"]

    def get(self, id, params=None, setup_log=False):

        if params is None:
            params = {}

        if setup_log is True:
            params["setup_log"] = "true"

        return super(K8sWorkerController, self).get(id, params)

    def set_storage(self, worker_id, ephemeral_disks=[], persistent_disks=[]):
        """Set storage for a k8s worker.

        Parameters
        ----------
        worker_id : str
            The k8s worker ID, format - '/api/v2/worker/k8shost/[0-9]+'
        ephemeral_disks : list
            List of ephemeral disks. Mandatory parameter, by default []
        persistent_disks : list, optional
            List of persistent disks, by default []

        Raises
        ------
        APIItemNotFoundException
        APIItemConflictException
        APIException
        AssertionError
        """
        # Make sure that the worker exists
        self.get(worker_id)

        assert isinstance(
            ephemeral_disks, list
        ), "'ephemeral_disks' must be provided and and must be a list"

        assert (
            len(ephemeral_disks) > 0
        ), "'ephemeral_disks' must contain at least one disk"

        assert isinstance(
            persistent_disks, list
        ), "'persistent_disks' must be a list"

        # Prepare the payload
        data = {
            "op_spec": {
                "ephemeral_disks": ephemeral_disks,
                "persistent_disks": persistent_disks,
            },
            "op": "storage",
        }

        # Make the request
        self.client._request(
            url=worker_id,
            http_method="post",
            data=data,
            description="worker/set_storage",
        )
