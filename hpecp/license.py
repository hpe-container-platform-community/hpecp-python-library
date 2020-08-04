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

import urllib

from requests.structures import CaseInsensitiveDict


class LicenseController:
    def __init__(self, client):
        self.client = client

    def platform_id(self):
        """Retrieve the Platform ID"""
        response = self.client._request(
            url="/api/v1/license",
            http_method="get",
            description="license/get_platform_id",
        )
        return response.json()["uuid"]

    def list(self):
        """Retrieve the list of licenses
        """
        response = self.client._request(
            url="/api/v2/hpelicense",
            http_method="get",
            description="license/get_license",
        )
        return response.json()

    def upload_with_ssh_key(
        self,
        server_filename,
        ssh_key_file=None,
        ssh_key_data=None,
        base64enc_license="",
    ):
        """Not implemented yet!

        Workaround:
         - scp your license to '/srv/bluedata/license/' on the controller
         - run client.license.register(server_filename) to register the license
        """
        raise Exception(
            "Not implemented yet! Workaround: scp your license to"
            " '/srv/bluedata/license/'"
        )

    def upload_with_ssh_pass(
        self, server_filename, ssh_username, ssh_password, base64enc_license=""
    ):
        """Not implemented yet!

        Workaround:
         - scp your license to '/srv/bluedata/license/' on the controller
         - run client.license.register(server_filename) to register the license
        """
        raise Exception(
            "Not implemented yet! Workaround: scp your license to"
            "'/srv/bluedata/license/'"
        )

    def register(self, server_filename):
        """Register a license. The license must have previously been uploaded
        to '/srv/bluedata/license/' on the controller.

        Parameters
        ----------
        server_filename: str
            Filepath to the license on the server, e.g.
            '/srv/bluedata/license/LICENSE-1.txt'

        Raises
        ------
        APIException
        """
        data = {"hpelicense_file": server_filename}
        response = self.client._request(
            url="/api/v2/hpelicense",
            http_method="post",
            data=data,
            description="license/register",
        )
        return CaseInsensitiveDict(response.headers)["Location"]

    def delete(self, license_key):
        """Delete a license by LicenseKey.

        Parameters
        ----------
        license_key: str
            The license key, e.g. '1234 1234 ... 1234 "SOMETEXT"'

        Raises
        ------
        APIException
        """

        try:
            lic = urllib.parse.quote(license_key)  # python 2
        except Exception:
            lic = urllib.pathname2url(license_key)  # python 3

        return self.client._request(
            url="/api/v2/hpelicense/{}/".format(lic),
            http_method="delete",
            description="license/delete",
        )
