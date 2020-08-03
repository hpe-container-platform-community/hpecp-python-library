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

from hpecp.base_resource import ResourceList

from .base_resource import AbstractResource, AbstractWaitableResourceController
from .exceptions import APIItemNotFoundException

try:
    basestring
except NameError:
    basestring = str


class GatewayStatus(Enum):
    """Bases: enum.Enum

    The statuses for a Gateway

    **Note:**

    The integer values do not have a meaning outside of this library.
    The API uses a string identifier with the status name rather than an
    integer value.
    """

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
    decommission_in_progress = 15
    delete_in_progress = 16


class Gateway(AbstractResource):
    """Create an instance of Gateway from json data returned from the HPE

    Container Platform API. Users of this library are not expected to create an
    instance of this class.

    Parameters
    ----------
    json : str
        The json returned by the API representing a Gateway.

    Returns
    -------
    Gateway
        An instance of Gateway
    """

    # All of the fields of Gateway objects as returned by the HPE Container
    # Platform API
    all_fields = [
        "id",
        "hacapable",
        "propinfo",
        "approved_worker_pubkey",
        "schedule",
        "ip",
        "proxy_nodes_hostname",
        "hostname",
        "state",
        "status_info",
        "purpose",
        "sysinfo",
        "tags",
    ]

    # These fields are displayed by default, e.g. in tabulate()
    default_display_fields = [
        "id",
        "ip",
        "proxy_nodes_hostname",
        "hostname",
        "state",
        "status_info",
        "purpose",
        "tags",
    ]

    @property
    def state(self):
        """@Field: from json['state']"""
        return self.json["state"]

    @property
    def hacapable(self):
        """@Field: from json['hacapable']"""
        return self.json["hacapable"]

    @property
    def propinfo(self):
        """@Field: from json['propinfo']"""
        return self.json["propinfo"]

    @property
    def approved_worker_pubkey(self):
        """@Field: from json['approved_worker_pubkey']"""
        return self.json["approved_worker_pubkey"]

    @property
    def schedule(self):
        """@Field: from json['schedule']"""
        return self.json["schedule"]

    @property
    def ip(self):
        """@Field: from json['ip']"""
        return self.json["ip"]

    @property
    def proxy_nodes_hostname(self):
        """@Field: from json['proxy_nodes_hostname']"""
        try:
            return self.json["proxy_nodes_hostname"]
        except KeyError:
            return ""

    @property
    def hostname(self):
        """@Field: from json['hostname']"""
        return self.json["hostname"]

    @property
    def purpose(self):
        """@Field: from json['purpose']"""
        return self.json["purpose"]

    @property
    def status_info(self):
        """@Field: from json['status_info']"""
        return self.json["status_info"]

    @property
    def sysinfo(self):
        """@Field: from json['sysinfo']"""
        return self.json["sysinfo"]

    @property
    def tags(self):
        """@Field: from json['tags']"""
        return self.json["tags"]


class GatewayController(AbstractWaitableResourceController):
    """Class that users will interact with to work with Gateways. An instance
    of this class is available in the
    client.ContainerPlatformClient with the attribute name
    :py:attr:`gateway <.client.ContainerPlatformClient.gateway>`. The methods
    of this class can be invoked using `client.gateway.method()`. See the
    example below:

    Example
    -------
    >>> client = ContainerPlatformClient(...).create_session()
    >>> client.gateway.list()
    """

    base_resource_path = "/api/v1/workers"

    resource_list_path = "workers"

    resource_class = Gateway

    status_class = GatewayStatus

    status_fieldname = "state"

    # def create_with_ssh_password(self, username, password):
    #     """Not Implemented yet"""
    #     raise NotImplementedError()

    def create_with_ssh_key(
        self, ip, proxy_node_hostname, ssh_key_data, tags=[]
    ):
        """Create a gateway instance using SSH key credentials to access the
        host.

        Parameters
        ----------
        ip: str
            The IP address of the proxy host.  Used for internal
            communication.
        proxy_node_hostname: str
            Clients will access cluster services will be accessed using
            this name.
        ssh_key_data: str
            The ssh key data as a string.
        tags: list
            Tags to use, e.g. "{ 'tag1': 'foo', 'tag2', 'bar' }".

        Returns
        -------
        str
            gateway ID
        """

        assert isinstance(
            ip, basestring
        ), "'ip' must be provided and must be a string"
        assert isinstance(
            proxy_node_hostname, basestring
        ), "'proxy_node_hostname' must be provided and must be a string"
        assert isinstance(
            ssh_key_data, basestring
        ), "'ssh_key_data' must be provided and must be a string"

        data = {
            "ip": ip,
            "credentials": {
                "type": "ssh_key_access",
                "ssh_key_data": ssh_key_data,
            },
            "tags": tags,
            "proxy_nodes_hostname": proxy_node_hostname,
            "purpose": "proxy",
        }

        response = self.client._request(
            url="/api/v1/workers/",
            http_method="post",
            data=data,
            description="gateway/create_with_ssh_key",
        )
        return CaseInsensitiveDict(response.headers)["location"]

    def get(self, id):
        """Retrieve a Gateway by ID.

        Parameters
        ----------
        id: str
            The gateway ID - format: '/api/v1/workers/[0-9]+'

        Returns
        -------
        Gateway
            object representing a Gateway

        Raises
        ------
        APIException
        """
        worker = super(GatewayController, self).get(id)
        if worker.purpose != "proxy":
            raise APIItemNotFoundException(
                message="gateway not found with id: " + id,
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
        resourceList = super(GatewayController, self).list()
        gateways = [gw for gw in resourceList.json if gw["purpose"] == "proxy"]
        return ResourceList(self.resource_class, gateways)

    # TODO refactor clients so implementation not required
    def wait_for_state(self, gateway_id, state=[], timeout_secs=1200):
        return super(GatewayController, self).wait_for_state(
            gateway_id, state, timeout_secs
        )
