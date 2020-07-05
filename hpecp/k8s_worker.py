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

from .base_resource import AbstractResourceController, AbstractResource

from enum import Enum

import polling

from .exceptions import APIItemNotFoundException

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

    # @staticmethod
    # def __class_dir__():
    #     return ["worker_id", "status", "hostname", "ipaddr", "href"]

    # def __repr__(self):
    #     return "<WorkerK8S worker_id:{} status:{} ipaddr:{}>".format(
    #         self.worker_id, self.status, self.ipaddr
    #     )

    # def __str__(self):
    #     return "WorkerK8s(worker_id={}, status={}, ipaddr={})".format(
    #         self.worker_id, self.status, self.ipaddr
    #     )

    # def __init__(self, json):
    #     self.json = json

    # def __dir__(self):
    #     return WorkerK8s.__class_dir__()

    # def __getitem__(self, item):
    #     return getattr(self, self.__dir__()[item])

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

    # def __len__(self):
    #     return len(dir(self))


# class WorkerK8sList:
#     def __init__(self, json):
#         self.json = json
#         self.tenants = sorted(
#             [WorkerK8s(t) for t in json], key=attrgetter("worker_id")
#         )

#     def __getitem__(self, item):
#         return self.tenants[item]

#     def next(self):
#         if not self.tenants:
#             raise StopIteration
#         return self.tenants.pop(0)

#     # TODO do we need  both next() and __next__()?
#     def __next__(self):
#         if not self.tenants:
#             raise StopIteration
#         return self.tenants.pop(0)

#     def __iter__(self):
#         return self

#     def __len__(self):
#         return len(self.tenants)

#     def tabulate(self, columns=None):
#         # FIXME columns is ignored, see GatewayController.list().tabulate()
#         # for an example implementation
#         return tabulate(
#             self, headers=WorkerK8s.__class_dir__(), tablefmt="pretty"
#         )


class K8sWorkerController(AbstractResourceController):

    base_resource_path = "/api/v2/worker/k8shost"

    resource_class = WorkerK8s

    def create_with_ssh_password(self, username, password):
        """Not Implemented yet"""
        raise NotImplementedError()

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
            description="worker/create_with_ssh_key",
        )
        return response.headers["location"]

    def list(self):
        return super(K8sWorkerController, self).list()

    def get(self, id, setup_log=False):
        return super(K8sWorkerController, self).get(id, None)

    def delete(self, id):
        super(K8sWorkerController, self).delete(id)

    # TODO rename status parameter to statuses
    def wait_for_status(self, worker_id, status=[], timeout_secs=1200):
        """Wait for K8S worker status.

        Parameters
        ----------
        worker_id: str
            The worker ID - format: '/api/v1/workers/[0-9]+'
        status: list[:py:class:`WorkerK8sStatus`]
            Status(es) to wait for.  Use an empty array if you want to
            wait for a cluster's existence to cease.
        timeout_secs: int
            How long to wait for the status(es) before raising an
            exception.

        Returns
        -------
        bool
            True if status was found before timeout, otherwise False

        Raises
        ------
        APIItemNotFoundException
            If the item is not found and status is not empty
            APIException: if a generic API exception occurred
        """
        self.get(worker_id)

        assert isinstance(status, list), "'status' must be a list"
        for i, s in enumerate(status):
            assert isinstance(
                s, WorkerK8sStatus
            ), "'status' item '{}' is not of type WorkerK8sStatus".format(i)
        assert isinstance(timeout_secs, int), "'timeout_secs' must be an int"
        assert timeout_secs >= 0, "'timeout_secs' must be >= 0"

        # if status is empty return success when worker_id not found
        if len(status) == 0:

            def item_not_exists():
                try:
                    self.get(worker_id)
                    return False
                except APIItemNotFoundException:
                    return True

            try:
                polling.poll(
                    lambda: item_not_exists(),
                    step=10,
                    poll_forever=False,
                    timeout=timeout_secs,
                )
                return True
            except polling.TimeoutException:
                return False

        # if state is not empty return success when gateway current state is
        # in desired state
        else:
            try:
                polling.poll(
                    lambda: self.get(worker_id).status
                    in [s.name for s in status],
                    step=10,
                    poll_forever=False,
                    timeout=timeout_secs,
                )
                return True
            except polling.TimeoutException:
                return False

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
