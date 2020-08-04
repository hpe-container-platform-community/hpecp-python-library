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
from hpecp.role import Role
from hpecp.cli import base


class RoleProxy(base.BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.role>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return ["delete", "examples", "get", "list"]

    def __init__(self):
        """Create instance of proxy class with the client module name."""
        super(RoleProxy, self).new_instance("role", Role)

    def examples(self):
        """Show examples for working with roles."""
        print(
            dedent(
                """\
                    
                # Retrieve the role ID for 'Admin'
                $ hpecp role list  --query "[?label.name == 'Admin'][_links.self.href] | [0][0]" --output json | tr -d '"'
                /api/v1/role/2
                """  # noqa:  E501
            )
        )
