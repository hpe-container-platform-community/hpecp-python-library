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

from mock import patch

from hpecp import ContainerPlatformClient

from .base import BaseTestCase
from .config_mock_api_responses import mockApiSetup

# setup the mock data
mockApiSetup()


class TestTentants(BaseTestCase):
    @patch("requests.post", side_effect=BaseTestCase.httpPostHandlers)
    def test_epic_tenant_list(self, mock_post):

        client = ContainerPlatformClient(
            username="admin",
            password="admin123",
            api_host="127.0.0.1",
            api_port=8080,
            use_ssl=True,
        )
        client.create_session()

        client.config.auth(
            {
                "external_identity_server": {
                    "bind_pwd": "5ambaPwd@",
                    "user_attribute": "sAMAccountName",
                    "bind_type": "search_bind",
                    "bind_dn": (
                        "cn=Administrator,CN=Users,DC=samdom"
                        ",DC=example,DC=com"
                    ),
                    "host": "1.1.1.1",
                    "security_protocol": "ldaps",
                    "base_dn": "CN=Users,DC=samdom,DC=example,DC=com",
                    "verify_peer": False,
                    "type": "Active Directory",
                    "port": 636,
                }
            }
        )
