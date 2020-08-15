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

from .base_resource import AbstractResource, AbstractResourceController


class Catalog(AbstractResource):
    """Catalog Image item."""

    # All of the fields of Catalog objects as returned by the HPE Container
    # Platform API.
    # TODO: Verify this with the specification
    all_fields = (
        "label_name",
        "label_description",
        "self_href",
        "feed",
        "distro_id",
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

    default_display_fields = [
        "label_name",
        "label_description",
        "self_href",
    ]

    # These fields are displayed by default, e.g. in tabulate()
    # TODO: Verify this with the specification
    # TODO: Pick a smaller subset, again based on the API response
    default_display_fields = all_fields

    @property
    def label_name(self):
        """@Field: from json['label']['name']"""
        try:
            return self.json["label"]["name"]
        except KeyError:
            return ""

    @property
    def label_description(self):
        """@Field: from json['label']['description']"""
        try:
            return self.json["label"]["description"]
        except KeyError:
            return ""

    @property
    def self_href(self):
        """@Field: from json['_links']['self']['href']"""
        try:
            return self.json["_links"]["self"]["href"]
        except KeyError:
            return ""

    @property
    def feed(self):
        """@Field: from json['_links']['feed']"""
        try:
            return self.json["_links"]["feed"]
        except KeyError:
            return ""

    @property
    def distro_id(self):
        """@Field: from json['distro_id']"""
        try:
            return self.json["distro_id"]
        except KeyError:
            return ""

    @property
    def version(self):
        """@Field: from json['version']"""
        try:
            return self.json["version"]
        except KeyError:
            return ""

    @property
    def timestamp(self):
        """@Field: from json['timestamp']"""
        try:
            return self.json["timestamp"]
        except KeyError:
            return ""

    @property
    def isdebug(self):
        """@Field: from json['isdebug']"""
        try:
            return self.json["isdebug"]
        except KeyError:
            return ""

    @property
    def osclass(self):
        """@Field: from json['osclass']"""
        try:
            return self.json["osclass"]
        except KeyError:
            return ""

    @property
    def logo_checksum(self):
        """@Field: from json['logo']['checksum']"""
        try:
            return self.json["logo"]["checksum"]
        except KeyError:
            return ""

    @property
    def logo_url(self):
        """@Field: from json['logo']['url']"""
        try:
            return self.json["logo"]["url"]
        except KeyError:
            return ""

    @property
    def documentation_checksum(self):
        """@Field: from json['documentation']['checksum']"""
        try:
            return self.json["documentation"]["checksum"]
        except KeyError:
            return ""

    @property
    def documentation_mimetype(self):
        """@Field: from json['documentation']['mimetype']"""
        try:
            return self.json["documentation"]["mimetype"]
        except KeyError:
            return ""

    @property
    def documentation_file(self):
        """@Field: from json['documentation']['file']"""
        try:
            return self.json["documentation"]["file"]
        except KeyError:
            return ""

    @property
    def state(self):
        """@Field: from json['state']"""
        try:
            return self.json["state"]
        except KeyError:
            return ""

    @property
    def state_info(self):
        """@Field: from json['state_info']"""
        try:
            return self.json["state_info"]
        except KeyError:
            return ""


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
