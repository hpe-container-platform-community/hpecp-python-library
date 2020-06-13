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
from operator import attrgetter

from tabulate import tabulate

try:
    basestring
except NameError:
    basestring = str


class Tenant:
    @staticmethod
    def __class_dir__():
        return ["id", "name", "description", "tenant_type"]

    def __repr__(self):
        return "<Tenant id:{} name:{} description:{} type:{}>".format(
            self.id, self.name, self.description, self.tenant_type
        )

    def __str__(self):
        return "Tenant(id={}, name={}, description={}, type:{})".format(
            self.id, self.name, self.description, self.tenant_type
        )

    def __init__(self, json):
        self.json = json

    def __dir__(self):
        return Tenant.__class_dir__()

    def __getitem__(self, item):
        return getattr(self, self.__dir__()[item])

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
            return None


class TenantList:
    """[summary]
    """

    def __init__(self, json):
        """[summary]

        Arguments:
            json {[type]} -- [description]
        """
        self.json = json
        self.tenants = sorted([Tenant(t) for t in json], key=attrgetter("id"))

    def __getitem__(self, item):
        return self.tenants[item]

    # Python 2
    def next(self):
        if not self.tenants:
            raise StopIteration
        return self.tenants.pop(0)

    # Python 3
    def __next__(self):
        if not self.tenants:
            raise StopIteration
        return self.tenants.pop(0)

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.tenants)

    def tabulate(self):
        """[summary]

        Returns:
            [type] -- [description]
        """
        return tabulate(
            self, headers=Tenant.__class_dir__(), tablefmt="pretty"
        )


class TenantController:
    """This class allows a user to retrieve and interact with tenant information

    An instance of this class is available in `client.ContainerPlatformClient`
    with the attribute name
    :py:attr:`tenant <.client.ContainerPlatformClient.tenant>`. The methods of
    this class can be invoked using `client.tenant.method()`. See the example
    below.

    Example::

        client = ContainerPlatformClient(...).create_session()
        client.tenant.list()
    """

    def __init__(self, client):
        self.client = client

    def list(self):
        """Retrieve a list of available tenants

        Returns:
            TenantList: list of tenants

        Raises:
            APIException
        """
        response = self.client._request(
            url="/api/v1/tenant", http_method="get", description="tenant/list"
        )
        tenants = TenantList(response.json()["_embedded"]["tenants"])
        return tenants

    def create(
        self, name=None, description=None, tenant_type=None, k8s_cluster=None
    ):

        self.client.log.warning(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )
        self.client.log.warning(
            "!!!! The method `tenant.create()` is experimental !!!!"
        )
        self.client.log.warning(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )

        assert (
            isinstance(name, basestring) and len(name) > 0
        ), "'name' must be provided and must be a string"
        assert description is None or isinstance(
            description, basestring
        ), "'description' if provided, must be a string"

        data = {
            "label": {"name": name},
            "tenant_type": tenant_type,
            "member_key_available": "all_admins",
            "k8s_cluster": k8s_cluster,
        }
        if description is not None:
            data["label"]["description"] = description

        response = self.client._request(
            url="/api/v1/tenant",
            http_method="post",
            data=data,
            description="tenant/create",
        )
        return response.headers["Location"]

    def get(self, tenant_id):
        """Retrieve a Tenant by ID.

        Args:
            tenant_id (str): The tenant ID - format: '/api/v1/tenant/[0-9]+'

        Returns:
            Tenat: object representing the Tenant

        Raises:
            APIException
        """
        self.client.log.warning(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )
        self.client.log.warning(
            "!!!! The method `tenant.get()` is experimental !!!!"
        )
        self.client.log.warning(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )

        assert isinstance(
            tenant_id, str
        ), "'tenant_id' must be provided and must be string"
        assert re.match(
            r"\/api\/v1\/tenant\/[0-9]+", tenant_id
        ), "'tenant_id' must have format '/api/v1/tenant/[0-9]+'"

        response = self.client._request(
            url=tenant_id, http_method="get", description="tenant/get"
        )
        return Tenant(response.json())

    def auth_setup(self, tenant_id, data):
        """summary

        Parameters:
            tenant_id : type
                description
            data : type
                description

        Example::

            data: {
                "external_user_groups": [
                    {
                        "role": "/api/v1/role/2", # 2 = Admins
                        "group":"CN=DemoTenantAdmins,CN=Users,DC=samdom
                        ,DC=example,DC=com"
                    },
                    {
                        "role": "/api/v1/role/3", # 3 = Members
                        "group": "CN=DemoTenantUsers,CN=Users,DC=samdom
                        ,DC=example,DC=com"
                    }
                ]
            }
        """
        self.client._request(
            url="/api/v1/tenant/{}?external_user_groups".format(tenant_id),
            http_method="put",
            data=data,
            description="epic_tenant_auth",
        )

    def assign_user_to_role(self, tenant_id, role_id, user_id):
        """Assign a user to a given role using the tenant

        Args:
            tenant_id (str): The tenant ID - format: '/api/v1/tenant/[0-9]+'
            role_id (str): The role ID - format: '/api/v1/role/[0-9]+'
            user_id (str): The role ID - format: '/api/v1/user/[0-9]+'

        Raises:
            APIItemNotFoundException
            APIItemConflictException
            APIException
        """
        # FIXME: Assuming this functionality is experimental like others.
        self.client.log.warning(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )
        self.client.log.warning(
            "!!!! The method `tenant.get()` is experimental !!!!"
        )
        self.client.log.warning(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )

        # Ensure that the tenant is valid and exists
        self.get(tenant_id)

        # Ensure that the role is valid and exists
        # FIXME: Uncomment this after the role is available with the client
        # self.client.role.get(role_id)

        # Ensure that the user is valid and exists
        self.client.user.get(user_id)

        # Build the request payload
        data = {
            "operation": "assign",
            "role": role_id,
            "user": user_id,
        }
        url = tenant_id + "?user"

        # Make the request
        self.client._request(
            url=url,
            http_method="put",
            data=data,
            description="assign_user_to_role",
        )
