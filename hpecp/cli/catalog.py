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

from hpecp import APIException
from hpecp.exceptions import APIItemNotFoundException
from textwrap import dedent
from hpecp.catalog import Catalog
from hpecp.cli import base


class CatalogProxy(base.BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.catalog>`."""

    def __init__(self):
        """Create instance of proxy class with the client module name."""
        super(CatalogProxy, self).new_instance("catalog", Catalog)

    def __dir__(self):
        """Return the CLI method names."""
        return [
            "get",
            "list",
            "delete",
            "examples",
            "wait_for_state",
            "refresh",
            "install",
        ]

    def delete(self, id):
        """Not implemented."""
        raise AttributeError("'CatalogProxy' object has no attribute 'delete'")

    def refresh(self, catalog_id):
        """Refresh a catalog.

        Parameters
        ----------
        catalog_id : str
            The ID of the catalog - format: '/api/v1/catalog/[0-9]+'

        Examples
        --------
        > hpecp catalog refresh /api/v1/catalog/99

        """
        try:
            base.get_client().catalog.refresh(catalog_id)

            # TODO: Report progress of the refresh workflow
        except AssertionError as ae:
            print(ae, file=sys.stderr)
            sys.exit(1)
        except (APIException, APIItemNotFoundException) as e:
            print(e.message, file=sys.stderr)
            sys.exit(1)

    def install(self, catalog_id):
        """Install a catalog.

        Parameters
        ----------
        catalog_id : str
            The ID of the catalog - format: '/api/v1/catalog/[0-9]+'

        Examples
        --------
        > hpecp catalog install /api/v1/catalog/99

        """
        try:
            base.get_client().catalog.install(catalog_id)

            # TODO: Implement a way to check if the installation is actually
            # successful (and maybe report progress?) - wait_for_state()?
        except AssertionError as ae:
            print(ae, file=sys.stderr)
            sys.exit(1)
        except (APIException, APIItemNotFoundException) as e:
            print(e.message, file=sys.stderr)
            sys.exit(1)

    def examples(self):
        """Show examples for working with roles."""
        print(
            dedent(
                """\

                $  hpecp catalog list --query "[?state!='installed' && state!='installing'] | [*].[_links.self.href] | []"  --output json
                ["/api/v1/catalog/24", "/api/v1/catalog/27", "/api/v1/catalog/14", "/api/v1/catalog/11", "/api/v1/catalog/28", "/api/v1/catalog/18"]

                $  hpecp catalog list --query "[?state!='installed' && state!='installing'] | [*].[_links.self.href] | []"  --output text
                /api/v1/catalog/24
                /api/v1/catalog/27
                /api/v1/catalog/14
                /api/v1/catalog/11
                /api/v1/catalog/28
                /api/v1/catalog/18

                $  hpecp catalog list --query "[?state!='installed' && state!='installing'] | [*].[_links.self.href, distro_id]"  --output text
                /api/v1/catalog/29	bluedata/spark240juphub7xssl
                /api/v1/catalog/11	bluedata/ubuntu16
                /api/v1/catalog/21	bluedata/cdh632multi
                /api/v1/catalog/2	bluedata/spark231juphub7xssl
                """  # noqa:  E501
            )
        )
