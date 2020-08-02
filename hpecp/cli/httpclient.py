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

from hpecp.cli import base


class HttpClientProxy(object):
    """Proxy object to :py:attr:`<hpecp.client._request>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return ["delete", "get", "post", "put"]

    @base.intercept_exception
    def get(
        self, url,
    ):
        """Make HTTP GET request.

        Examples
        --------
        $ hpecp httpclient get /api/v1/workers
        """
        response = base.get_client()._request(
            url, http_method="get", description="CLI HTTP GET",
        )
        print(response.text, file=sys.stdout)

    @base.intercept_exception
    def delete(
        self, url,
    ):
        """Make HTTP DELETE request.

        Examples
        --------
        $ hpecp httpclient delete /api/v1/workers/1
        """
        base.get_client()._request(
            url, http_method="delete", description="CLI HTTP DELETE",
        )

    @base.intercept_exception
    def post(
        self, url, json_file="",
    ):
        """Make HTTP POST request.

        Examples
        --------
        $ cat > my.json <<-EOF
            {
                "external_identity_server":  {
                    "bind_pwd":"5ambaPwd@",
                    "user_attribute":"sAMAccountName",
                    "bind_type":"search_bind",
                    "bind_dn":"cn=Administrator,CN=Users,DC=samdom,DC=example,DC=com",
                    "host":"10.1.0.77",
                    "security_protocol":"ldaps",
                    "base_dn":"CN=Users,DC=samdom,DC=example,DC=com",
                    "verify_peer": false,
                    "type":"Active Directory",
                    "port":636
                }
            }
            EOF

            hpecp httpclient post /api/v2/config/auth --json-file my.json
        """
        with open(json_file, "r",) as f:
            data = json.load(f)

        response = base.get_client()._request(
            url, http_method="post", data=data, description="CLI HTTP POST",
        )
        print(response.text, file=sys.stdout)

    @base.intercept_exception
    def put(
        self, url, json_file="",
    ):
        """Make HTTP PUT request.

        Examples
        --------
        $ hpecp httpclient put /api/v2/config/auth --json-file my.json
        """  # noqa: W293
        with open(json_file, "r",) as f:
            data = json.load(f)

        response = base.get_client()._request(
            url, http_method="put", data=data, description="CLI HTTP PUT",
        )
        print(response.text, file=sys.stdout)
