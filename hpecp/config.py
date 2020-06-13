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


class ConfigController:
    def __init__(self, client):
        self.client = client

    def auth(self, data):
        """
        Example::
            data = {
                "external_identity_server":  {
                    "bind_pwd":"5ambaPwd@",
                    "user_attribute":"sAMAccountName",
                    "bind_type":"search_bind",
                    "bind_dn":"cn=Administrator,CN=Users,DC=samdom,DC=example,DC=com",
                    "host":"10.1.0.77",
                    "security_protocol":"ldaps",
                    "base_dn":"CN=Users,DC=samdom,DC=example,DC=com",
                    "verify_peer": False,
                    "type":"Active Directory",
                    "port":636
                }
            }
        """
        self.client._request(
            url="/api/v2/config/auth",
            http_method="post",
            data=data,
            description="config/auth",
        )
