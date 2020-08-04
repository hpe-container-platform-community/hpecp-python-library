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

import sys
from hpecp.gateway import Gateway, GatewayStatus
from hpecp.cli import base


class GatewayProxy(base.BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.gateway>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return [
            "create_with_ssh_key",
            "delete",
            "get",
            "list",
            "states",
            "wait_for_state",
        ]

    def __init__(self):
        """Create instance of proxy class with the client module name."""
        super(GatewayProxy, self).new_instance("gateway", Gateway)

    @base.intercept_exception
    def create_with_ssh_key(
        self,
        ip,
        proxy_node_hostname,
        ssh_key=None,
        ssh_key_file=None,
        tags=[],
    ):
        """Create a Gateway using SSH key authentication.

        Parameters
        ----------
        ip : string
            The IP address of the proxy host.  Used for internal
            communication.
        proxy_node_hostname: string
            Clients will access cluster services will be accessed
            using this name.
        ssh_key: string
            The ssh key data as a string.  Alternatively, use the
            ssh_key_file parameter.
        ssh_key_file: string
            The file path to the ssh key.  Alternatively, use the
            ssh_key parameter.
        tags: string
            Tags to add to the gateway, for example:
            "{ 'tag1': 'foo', 'tag2', 'bar' }".
        """
        if ssh_key is None and ssh_key_file is None:
            print(
                "Either ssh_key or ssh_key_file must be provided",
                file=sys.stderr,
            )
            sys.exit(1)

        if ssh_key is not None and ssh_key_file is not None:
            print(
                "Either ssh_key or ssh_key_file must be provided",
                file=sys.stderr,
            )
            sys.exit(1)

        if ssh_key_file:
            with open(ssh_key_file) as f:
                ssh_key = f.read()

        gateway_id = base.get_client().gateway.create_with_ssh_key(
            ip=ip,
            proxy_node_hostname=proxy_node_hostname,
            ssh_key_data=ssh_key,
            tags=tags,
        )
        print(gateway_id)

    def states(self,):
        """Return a list of valid states."""
        print([s.name for s in GatewayStatus])
