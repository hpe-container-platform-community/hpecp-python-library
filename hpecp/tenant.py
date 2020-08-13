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

from hpecp.base_resource import ResourceList
from hpecp.exceptions import ContainerPlatformClientException
from hpecp.user import User

from .base_resource import AbstractResource, AbstractWaitableResourceController

try:
    basestring
except NameError:
    basestring = str


class TenantStatus(Enum):
    """Bases: enum.Enum

    The statuses for Tenant

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


class Tenant(AbstractResource):

    all_fields = [
        "id",
        "name",
        "description",
        "status",
        "tenant_type",
        "external_user_groups",
    ]

    default_display_fields = [
        "id",
        "name",
        "description",
        "status",
        "tenant_type",
    ]

    @property
    def id(self):
        return self.json["_links"]["self"]["href"]

    @property
    def status(self):
        return self.json["status"]

    @property
    def name(self):
        return self.json["label"]["name"]

    @property
    def description(self):
        return self.json["label"]["description"]

    @property
    def tenant_type(self):
        try:
            return self.json["tenant_type"]
        except KeyError:
            return ""

    @property
    def external_user_groups(self):
        try:
            return self.json["external_user_groups"]
        except KeyError:
            return ""


class TenantController(AbstractWaitableResourceController):
    """Class that users will interact with to work with tenants.

    An instance of this class is available in
    `client.ContainerPlatformClient` with the attribute name
    :py:attr:`tenant <.client.ContainerPlatformClient.tenant>`. The methods of
    this class can be invoked using `client.tenant.method()`. See the example
    below.

    Example
    -------
    >>> client = ContainerPlatformClient(...).create_session()
    >>> client.tenant.list()
    """

    base_resource_path = "/api/v1/tenant/"
    resource_class = Tenant
    resource_list_path = "tenants"
    status_class = TenantStatus
    status_fieldname = "status"

    def __init__(self, client):
        self.client = client

    def create(
        self,
        name=None,
        description=None,
        tenant_type=None,
        k8s_cluster_id=None,
    ):

        assert (
            isinstance(name, basestring) and len(name) > 0
        ), "'name' must be provided and must be a string"
        assert description is None or isinstance(
            description, basestring
        ), "'description' if provided, must be a string"

        assert isinstance(k8s_cluster_id, str) and re.match(
            r"\/api\/v2\/k8scluster\/[0-9]+", k8s_cluster_id
        ), "'k8s_cluster_id' must have format '/api/v2/k8scluster/[0-9]+'"

        data = {
            "label": {"name": name},
            "tenant_type": tenant_type,
            "member_key_available": "all_admins",
            "k8s_cluster": k8s_cluster_id,
        }
        if description is not None:
            data["label"]["description"] = description

        response = self.client._request(
            url="/api/v1/tenant",
            http_method="post",
            data=data,
            description="tenant/create",
        )
        return CaseInsensitiveDict(response.headers)["Location"]

    def k8skubeconfig(self):
        """Retrieve the tenant kubeconfig.

        This requires the ContainerPlatformClient to be created with
        a 'tenant' parameter.

        Returns
        -------
        str
            Tenant KubeConfig

        Raises
        ------
        ContainerPlatformClientException
            This is raised if the ContainerPlatformClient was not created with
            a 'tenant' parameter.
        """
        if self.client.tenant_config is None:
            raise ContainerPlatformClientException(
                "'tenant' session is required, but client "
                "was not create with a 'tenant' argument."
            )
        response = self.client._request(
            url="/api/v2/k8skubeconfig/",
            http_method="get",
            description="tenant/k8skubeconfig",
        )
        return response.text

    def get_external_user_groups(self, tenant_id):
        return self.get(tenant_id).external_user_groups

    def delete_external_user_group(
        self, tenant_id, group,
    ):
        user_groups = self.get_external_user_groups(tenant_id)

        # if group exists already, remove it
        user_groups = [
            ug for ug in user_groups if ug["group"].lower() != group.lower()
        ]

        data = {"external_user_groups": user_groups}
        self.client._request(
            url=tenant_id + "?external_user_groups",
            http_method="put",
            data=data,
            description="tenant/add_external_user_groups",
        )

    def add_external_user_group(
        self, tenant_id, group, role_id,
    ):
        user_groups = self.get_external_user_groups(tenant_id)

        # if group exists already, remove it
        user_groups = [ug for ug in user_groups if ug["group"] != group]

        # add group
        user_groups.append({"group": group, "role": role_id})

        data = {"external_user_groups": user_groups}
        self.client._request(
            url=tenant_id + "?external_user_groups",
            http_method="put",
            data=data,
            description="tenant/add_external_user_groups",
        )

    def users(self, id):
        response = self.client._request(
            url=id + "?user", http_method="get", description="tenant/users",
        )
        return ResourceList(User, response.json()["_embedded"]["users"],)

    def assign_user_to_role(self, tenant_id, role_id, user_id):
        """Assign a user to a given role using the tenant.

        Parameters
        ----------
        tenant_id : str
            The tenant ID - format: '/api/v1/tenant/[0-9]+'
        role_id : str
            The role ID - format: '/api/v1/role/[0-9]+'
        user_id : str
            The role ID - format: '/api/v1/user/[0-9]+'

        Raises
        ------
        APIItemNotFoundException
        APIItemConflictException
        APIException
        """
        # Ensure that the tenant is valid and exists
        self.get(tenant_id)

        # Ensure that the role is valid and exists
        self.client.role.get(role_id)

        # Ensure that the user is valid and exists
        self.client.user.get(user_id)

        data = {"operation": "assign", "role": role_id, "user": user_id}
        url = tenant_id + "?user"

        # Make the request
        self.client._request(
            url=url,
            http_method="put",
            data=data,
            description="assign_user_to_role",
        )

    def revoke_user_from_role(self, tenant_id, role_id, user_id):
        # Ensure that the tenant is valid and exists
        self.get(tenant_id)

        # Ensure that teh role is valid and exists
        self.client.role.get(role_id)

        # Ensure that the user is valid and exists
        self.client.user.get(user_id)

        data = {"operation": "revoke", "role": role_id, "user": user_id}
        url = tenant_id + "?user"

        # Make the request
        self.client._request(
            url=url,
            http_method="put",
            data=data,
            description="revoke_user_from_role",
        )
