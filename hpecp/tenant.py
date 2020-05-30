from __future__ import absolute_import

from .logger import Logger

import textwrap
from operator import attrgetter
from tabulate import tabulate
import requests
import json
import sys

try:
    basestring
except NameError:
    basestring = str


class Tenant:
    @staticmethod
    def __class_dir__():
        return ["id", "name", "description", "tenant_type"]

    def __repr__(self):
        return "<Tenant id:{} name:{} description:{}>".format(
            self.id, self.name, self.description, self.tenant_type
        )

    def __str__(self):
        return "Tenant(id={}, name={}, description={})".format(
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
    """[summary]
    """

    def __init__(self, client):
        self.client = client

    def list(self):
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

        self.client.log.warning(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )
        self.client.log.warning(
            "!!!! The method `tenant.get()` is experimental !!!!"
        )
        self.client.log.warning(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )

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

            data =  {"external_user_groups":[
                {
                    "role":"/api/v1/role/2", # 2 = Admins
                    "group":"CN=DemoTenantAdmins,CN=Users,DC=samdom,DC=example,DC=com"
                },
                { 
                    "role":"/api/v1/role/3", # 3 = Members
                    "group":"CN=DemoTenantUsers,CN=Users,DC=samdom,DC=example,DC=com"
                }]}
        """
        self.client._request(
            url="/api/v1/tenant/{}?external_user_groups".format(tenant_id),
            http_method="put",
            data=data,
            description="epic_tenant_auth",
        )
