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

"""HPE Container Platform CLI."""

from __future__ import print_function

from textwrap import dedent
from hpecp.tenant import Tenant
from hpecp.cli import base


class TenantProxy(base.BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.tenant>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return [
            "add_external_user_group",
            "assign_user_to_role",
            "create",
            "delete",
            "delete_external_user_group",
            "examples",
            "get",
            "get_external_user_groups",
            "k8skubeconfig",
            "list",
            # "status",  # TODO: implement me!
            "users",
            "wait_for_status",
        ]

    def __init__(self):
        """Create instance of proxy class with the client module name."""
        super(TenantProxy, self).new_instance("tenant", Tenant)

    @base.intercept_exception
    def create(
        self,
        name=None,
        description=None,
        tenant_type=None,
        k8s_cluster_id=None,
    ):
        """Create a tenant.

        Parameters
        ----------
        name : [type], optional
            [description], by default None
        description : [type], optional
            [description], by default None
        tenant_type : [type], optional
            [description], by default None
        k8s_cluster_id : [type], optional
            [description], by default None
        """
        tenant_id = base.get_client().tenant.create(
            name=name,
            description=description,
            tenant_type=tenant_type,
            k8s_cluster_id=k8s_cluster_id,
        )
        print(tenant_id)

    def examples(self):
        """Show usage_examples of the list method."""
        print(
            dedent(
                """\

                hpecp tenant list --query "[?tenant_type == 'k8s']" --output json-pp

                """  # noqa: E501
            )
        )

    @base.intercept_exception
    def k8skubeconfig(self):
        """Retrieve the tenant kubeconfig.

        This requires the ContainerPlatformClient to be created with
        a 'tenant' parameter.

        Returns
        -------
        str
            Tenant KubeConfig
        """
        conf = base.get_client().tenant.k8skubeconfig()
        print(conf)

    @base.intercept_exception
    def users(self, id, output="table", columns="ALL", query={}):
        """Retrieve users assigned to tenant.

        Parameters
        ----------
        id : str
            The tenant ID.
        """
        list_instance = base.get_client().tenant.users(id=id)
        self.print_list(
            list_instance=list_instance,
            output=output,
            columns=columns,
            query=query,
        )

    @base.intercept_exception
    def assign_user_to_role(self, tenant_id, user_id, role_id):
        """Assign user to role in tenant."""
        base.get_client().tenant.assign_user_to_role(
            tenant_id=tenant_id, user_id=user_id, role_id=role_id
        )

    @base.intercept_exception
    def get_external_user_groups(self, tenant_id):
        """Retrieve External User Groups."""
        print(
            base.get_client().tenant.get_external_user_groups(
                tenant_id=tenant_id
            )
        )

    @base.intercept_exception
    def add_external_user_group(self, tenant_id, group, role_id):
        """Add External User Group."""
        base.get_client().tenant.add_external_user_group(
            tenant_id=tenant_id, group=group, role_id=role_id
        )

    @base.intercept_exception
    def delete_external_user_group(self, tenant_id, group):
        """Delete External User Group."""
        base.get_client().tenant.delete_external_user_group(
            tenant_id=tenant_id, group=group
        )
