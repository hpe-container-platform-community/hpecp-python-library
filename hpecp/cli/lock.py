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

import json
import sys
import yaml

from hpecp.cli import base


class LockProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.lock>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return [
            "create",
            "delete",
            "delete_all",
            "list",
        ]

    def list(
        self, output="yaml",
    ):
        """Get the system and user locks.

        :param output: how to display the output ['yaml'|'json']
        """
        if output not in ["yaml", "json"]:
            print(
                "'output' parameter must be 'yaml' or 'json'", file=sys.stderr
            )
            sys.exit(1)

        response = base.get_client().lock.get()

        if output == "yaml":
            print(
                yaml.dump(
                    yaml.load(json.dumps(response), Loader=yaml.FullLoader,)
                )
            )
        else:
            print(json.dumps(response))

    @base.intercept_exception
    def create(
        self, reason,
    ):
        """Create a lock."""
        print(base.get_client().lock.create(reason), file=sys.stdout)

    @base.intercept_exception
    def delete(
        self, id,
    ):
        """Delete a user lock."""
        base.get_client().lock.delete(id)

    @base.intercept_exception
    def delete_all(
        self, timeout_secs=300,
    ):
        """Delete all locks."""
        success = base.get_client().lock.delete_all(timeout_secs=timeout_secs)
        if not success:
            print("Could not delete locks.", file=sys.stderr)
            sys.exit(1)
