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
from hpecp.user import User
from hpecp.cli import base


class UserProxy(base.BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.user>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return ["create", "get", "delete", "examples", "list"]

    def __init__(self):
        """Create instance of proxy class with the client module name."""
        super(UserProxy, self).new_instance("user", User)

    @base.intercept_exception
    def create(
        self, name, password, description, is_external=False,
    ):
        """Create a User.

        :param name: the user name
        :param password:  the password
        :param description: the user descripton

        """
        user_id = base.get_client().user.create(
            name=name,
            password=password,
            description=description,
            is_external=is_external,
        )
        print(user_id)

    def examples(self):
        """Show usage_examples of the list method."""
        print(
            dedent(
                """\

                hpecp user list --query '[?is_external]' --output json-pp
                """  # noqa: E501
            )
        )
