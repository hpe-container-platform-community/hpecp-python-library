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

from hpecp.exceptions import APIItemNotFoundException

from .base_resource import (
    AbstractResource,
    AbstractWaitableResourceController,
    ResourceList,
)

try:
    basestring
except NameError:
    basestring = str


class WorkerEpicStatus(Enum):
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


class WorkerEpic(AbstractResource):

    all_fields = [
        "id",
        "state",
        "ip",
        "purpose",
        "href",
        "_links",
    ]
    """All of the fields of a Epic Cluster objects that are returned by the HPE
    Container Platform API"""

    default_display_fields = ["id", "state", "ip", "purpose"]

    @property
    def worker_id(self):
        return int(self.json["_links"]["self"]["href"].split("/")[-1])

    @property
    def state(self):
        return self.json["state"]

    @property
    def hostname(self):
        return self.json["hostname"]

    @property
    def ip(self):
        return self.json["ip"]

    @property
    def purpose(self):
        """@Field: from json['purpose']"""
        return self.json["purpose"]

    @property
    def href(self):
        return self.json["_links"]["self"]["href"]


class EpicWorkerController(AbstractWaitableResourceController):

    base_resource_path = "/api/v1/workers"

    resource_list_path = "workers"

    resource_class = WorkerEpic

    status_class = WorkerEpicStatus

    status_fieldname = "state"

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
            "ip": ip,
            "credentials": {
                "type": "ssh_key_access",
                "ssh_key_data": ssh_key_data,
            },
            "purpose": "worker",
            "tags": tags,
        }

        response = self.client._request(
            url="/api/v1/workers/",
            http_method="post",
            data=data,
            description="EpicWorkerController/create_with_ssh_key",
        )
        return CaseInsensitiveDict(response.headers)["location"]

    def get(self, id, params={}):
        """Retrieve an EPIC Worker by ID.

        Parameters
        ----------
        id: str
            The worker ID - format: '/api/v1/workers/[0-9]+'

        Returns
        -------
        EPIC Worker
            object representing an EPIC Worker

        Raises
        ------
        APIException
        """
        worker = super(EpicWorkerController, self).get(id, params)
        if worker.purpose != "worker":
            raise APIItemNotFoundException(
                message="worker not found with id: " + id,
                request_method="get",
                request_url=id,
            )
        return worker

    def list(self):
        """Make an API call to retrieve a list of Resources.

        Returns
        -------
        ResourceList
            The ResourceList will contain instances of the class defined by
            the property self.resource_class
        """
        resourceList = super(EpicWorkerController, self).list()
        workers = [
            wkr for wkr in resourceList.json if wkr["purpose"] == "worker"
        ]
        return ResourceList(self.resource_class, workers)

    def set_storage(self, worker_id, ephemeral_disks=[], persistent_disks=[]):
        """Set storage for a Epic worker.

        Parameters
        ----------
        worker_id : str
            The Epic worker ID, format - '/api/v1/worker/[0-9]+'
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

        data = {
            "workers": [
                {
                    "containerdisks": ephemeral_disks,
                    "hdfsdisks": persistent_disks,
                    "id": worker_id,
                }
            ]
        }

        # Make the request
        self.client._request(
            url="/api/v1/install/?install_alter",
            http_method="put",
            data=data,
            description="worker/set_storage",
        )
