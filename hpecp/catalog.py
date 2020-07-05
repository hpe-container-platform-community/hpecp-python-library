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

from .base_resource import AbstractResourceController, AbstractResource


class Catalog(AbstractResource):
    """Catalog Image item."""

    # All of the fields of Catalog objects as returned by the HPE Container
    # Platform API.
    # TODO: Verify this with the specification
    all_fields = (
        "label_name",
        "label_description",
        "self_href",
        "feed_href",
        "feed_name",
        "distro_id",
        "name",
        "description",
        "version",
        "timestamp",
        "isdebug",
        "osclass",
        "logo_checksum",
        "logo_url",
        "documentation_checksum",
        "documentation_mimetype",
        "documentation_file",
        "state",
        "state_info",
    )

    # These fields are displayed by default, e.g. in tabulate()
    # TODO: Verify this with the specification
    # TODO: Pick a smaller subset, again based on the API response
    default_display_fields = all_fields

    @property
    def distro_id(self):
        """@Field: from json['distro_id']"""
        return self.json["distro_id"]

    @property
    def state(self):
        """@Field: from json['state']"""
        return self.json["state"]


class CatalogController(AbstractResourceController):
    """Class that users will interact with to work with catalogs

    An instance of this class is available in the
    `client.ContainerPlatformClient` with the attribute name
    :py:attr:`catalog <.client.ContainerPlatformClient.catalog>`. The methods
    of this class can be invoked using `client.catalog.method()`. See the
    example below:

    Examples
    --------
    >>> client = ContainerPlatformClient(...).create_session()
    >>> client.catalog.list()
    """

    base_resource_path = "/api/v1/catalog"

    resource_list_path = "independent_catalog_entries"

    resource_class = Catalog

    def install(self, catalog_id):
        """Install the specified catalog.

        Parameters
        ----------
        catalog_id : str
            The ID of the catalog - format /api/v1/catalog/[0-9]+

        Raises
        ------
        APIItemNotFoundException
        APIItemConflictException
        APIException
        """
        # Make sure that the given catalog exists, other validations will also
        # be taken care of.
        self.get(catalog_id)

        _data = {"action": "install"}

        self.client._request(
            url=catalog_id,
            http_method="post",
            description="catalog/post/install",
            data=_data,
        )

    def refresh(self, catalog_id):
        """Refresh the specified catalog.

        Parameters
        ----------
        catalog_id : str
            The ID of the catalog - format /api/v1/catalog/[0-9]+

        Raises
        ------
        APIItemNotFoundException
        APIItemConflictException
        APIException
        """
        # Make sure that the given catalog exists, other validations will also
        # be taken care of.
        self.get(catalog_id)

        _data = {"action": "refresh"}

        self.client._request(
            url=catalog_id,
            http_method="post",
            description="catalog/post/refresh",
            data=_data,
        )
