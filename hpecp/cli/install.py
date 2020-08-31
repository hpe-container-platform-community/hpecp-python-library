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
import jmespath
import sys
import yaml
from textwrap import dedent

from hpecp.cli import base
from hpecp.cli_utils import TextOutput


class InstallProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.install>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return ["examples", "get", "set_gateway_ssl"]

    @base.intercept_exception
    def get(self, output="yaml", query=None):
        """Get the system config.

        :param output: how to display the output '[yaml|json|json-pp]'
        """
        if output not in ["yaml", "json", "json-pp", "text"]:
            print(
                (
                    "'output' parameter must be 'yaml', 'json', "
                    "'json-pp' or 'text'."
                ),
                file=sys.stderr,
            )
            sys.exit(1)

        if output == "yaml" and query is not None:
            print(
                "output=yaml is not supported with the query parameter.",
                file=sys.stderr,
            )
            sys.exit(1)

        response = base.get_client().install.get()

        if output == "yaml":
            print(
                yaml.dump(
                    yaml.load(
                        json.dumps(response),
                        Loader=yaml.FullLoader,
                    )
                )
            )
        else:
            if query is None:
                data = response
            else:
                data = jmespath.search(str(query), response)

            if output == "json-pp":
                print(json.dumps(data, indent=4, sort_keys=True))
            elif output == "text":
                print(TextOutput.dump(data))
            else:
                print(json.dumps(data))

    def examples(self):
        """Show examples for working with roles."""
        print(
            dedent(
                """\

                """  # noqa:  E501
            )
        )

    @base.intercept_exception
    def set_gateway_ssl(
        self,
        cert_file=None,
        cert_content=None,
        cert_file_name=None,
        key_file=None,
        key_content=None,
        key_file_name=None,
    ):
        """Set Gateway SSL.

        Parameters
        ----------
        cert_file : [type]
            [description]
        cert_content : [type]
            [description]
        cert_file_name : [type]
            [description]
        key_file : [type]
            [description]
        key_content : [type]
            [description]
        key_file_name : [type]
            [description]
        """
        assert (
            cert_file is None
            and (cert_content is not None and cert_file_name is not None)
        ) or (
            cert_file is not None
            and (cert_content is None and cert_file_name is None)
        ), (
            "('cert-content' and 'cert-file-name') or 'cert-file' "
            "must be provided."
        )

        assert (
            key_file is None
            and (key_content is not None and key_file_name is not None)
        ) or (
            key_file is not None
            and (key_content is None and key_file_name is None)
        ), (
            "('key_content' and 'key_file-name') or 'key_file' "
            "must be provided."
        )

        if cert_file:
            try:
                with open(cert_file, "r") as f:
                    cert_content = (
                        f.read().replace("\n", "\n").replace("\t", "\t")
                    )
                cert_file_name = cert_file
            except OSError:
                print(
                    "Could not open/read 'cert-file': {}".format(cert_file),
                    file=sys.stderr,
                )
                sys.exit(1)

        if key_file:
            try:
                with open(key_file, "r") as f:
                    key_content = (
                        f.read().replace("\n", "\n").replace("\t", "\t")
                    )
                key_file_name = key_file
            except OSError:
                print(
                    "Could not open/read 'key-file': {}".format(key_file),
                    file=sys.stderr,
                )
                sys.exit(1)

        base.get_client().install.set_gateway_ssl(
            cert_content, cert_file_name, key_content, key_file_name
        )
