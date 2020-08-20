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
from hpecp.datatap import Datatap
from hpecp.cli import base


class DatatapProxy(base.BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.datatap>`."""

    def __init__(self):
        """Create instance of proxy class with the client module name."""
        super(DatatapProxy, self).new_instance("datatap", Datatap)

    def __dir__(self):
        """Return the CLI method names."""
        return [
            "create_hdfs_with_kerberos",
            "get",
            "list",
            "delete",
            # "examples",
            "wait_for_state",
        ]

    def examples(self):
        """Show examples for working with roles."""
        print(
            dedent(
                """\
                    Coming soon ...
                """  # noqa:  E501
            )
        )

    def create_hdfs_with_kerberos(
        self,
        name,
        description,
        path_from_endpoint,
        kdc_data_host,
        kdc_data_port,
        realm,
        client_principal,
        browse_only,
        host,
        keytab,
        service_id,
        backup_host,
        endpoint_type,
        endpoint_port,
        read_only,
    ):
        """TODO.

        Parameters
        ----------
        name : [type]
            [description]
        description : [type]
            [description]
        path_from_endpoint : [type]
            [description]
        kdc_data_host : [type]
            [description]
        kdc_data_port : [type]
            [description]
        realm : [type]
            [description]
        client_principal : [type]
            [description]
        browse_only : [type]
            [description]
        host : [type]
            [description]
        keytab : [type]
            [description]
        service_id : [type]
            [description]
        backup_host : [type]
            [description]
        endpoint_type : [type]
            [description]
        endpoint_port : [type]
            [description]
        read_only : [type]
            [description]
        """
        base.get_client().datatap.create(
            name,
            description,
            path_from_endpoint,
            kdc_data_host,
            kdc_data_port,
            realm,
            client_principal,
            browse_only,
            host,
            keytab,
            service_id,
            backup_host,
            endpoint_type,
            endpoint_port,
            read_only,
        )
