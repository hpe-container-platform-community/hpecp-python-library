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

if sys.version_info[0] >= 3:
    unicode = str


class LicenseProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.license>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return ["delete", "delete_all", "list", "platform_id", "register"]

    @base.intercept_exception
    def platform_id(self,):
        """Get the platform ID."""
        print(base.get_client().license.platform_id())

    def list(
        self, output="yaml", license_key_only=False,
    ):
        """Retrieve the list of licenses.

        :param output: how to display the output ['yaml'|'json']
        """
        response = base.get_client().license.list()
        if license_key_only:
            response = [
                str(unicode(li["LicenseKey"])) for li in response["Licenses"]
            ]
            print("\n".join(response))
        else:
            if output == "yaml":
                print(
                    yaml.dump(
                        yaml.load(
                            json.dumps(response), Loader=yaml.FullLoader,
                        )
                    )
                )
            else:
                print(json.dumps(response))

    @base.intercept_exception
    def register(
        self, server_filename,
    ):
        """Register a license.

        :param server_filename: Filepath to the license on the server, e.g.
            '/srv/bluedata/license/LICENSE-1.txt'
        """
        print(
            base.get_client().license.register(server_filename=server_filename)
        )

    # TODO implement me!
    # def upload_with_ssh_key(
    #     self,
    #     server_filename,
    #     ssh_key_file=None,
    #     ssh_key_data=None,
    #     license_file=None,
    #     base64enc_license_data=None,
    # ):
    #     """Not implemented yet.

    #     Workaround:
    #     -----------
    #      - scp your license to '/srv/bluedata/license/' on the controller
    #      - run client.license.register(server_filename) to register
    #        the license
    #     """
    #     raise Exception(
    #         "Not implemented yet! Workaround: scp your license to"
    #         "'/srv/bluedata/license/'"
    #     )

    # TODO implement me!
    # def upload_with_ssh_pass(
    #     self,
    #     server_filename,
    #     ssh_username,
    #     ssh_password,
    #     license_file=None,
    #     base64enc_license_data=None,
    # ):
    #     """Not implemented yet.

    #     Workaround:
    #     -----------
    #      - scp your license to '/srv/bluedata/license/' on the controller
    #      - run client.license.register(server_filename) to register
    #        the license
    #     """
    #     raise Exception(
    #         "Not implemented yet! Workaround: scp your license to"
    #         "'/srv/bluedata/license/'"
    #     )

    @base.intercept_exception
    def delete(
        self, license_key,
    ):
        """Delete a license by LicenseKey.

        :param license_key: The license key, e.g. '1234 1234 ... 1234
            "SOMETEXT"'
        """
        base.get_client().license.delete(license_key=license_key)

    @base.intercept_exception
    def delete_all(self,):
        """Delete all licenses."""
        response = base.get_client().license.list()
        all_license_keys = [
            str(unicode(li["LicenseKey"])) for li in response["Licenses"]
        ]
        for licence_key in all_license_keys:
            base.get_client().license.delete(license_key=licence_key)
