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

import re
from operator import attrgetter

from tabulate import tabulate


class CatalogController:
    """Class that users will interact with to work with catalogs.

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

    def __init__(self, client):
        self.client = client

    def list(self):
        """Retrieve a list of Catalogs.

        Returns
        -------
        CatalogList
            list of Catalogs

        Raises
        ------
        APIException
        """
        response = self.client._request(
            url="/api/v1/catalog/",
            http_method="get",
            description="catalog/list",
        )
        return CatalogList(
            response.json()["_embedded"]["independent_catalog_entries"]
        )

    def get(self, catalog_id):
        """Retrieve a catalog identified by {catalog_id}.

        Parameters
        ----------
        catalog_id: str
            The Catalog ID - format: '/api/v1/catalog/[0-9]+'

        Returns
        -------
        Catalog
            object representing the requested Catalog

        Raises
        ------
        APIException
        APIItemNotFoundException
        """
        assert isinstance(
            catalog_id, str
        ), "'catalog_id' must be provided and must be a string"
        assert re.match(
            r"\/api\/v1\/catalog\/[0-9]+", catalog_id
        ), "'catalog_id' must have format '/api/v1/catalog/[0-9]+'"

        response = self.client._request(
            url=catalog_id, http_method="get", description="catalog/get"
        )

        return Catalog(response.json())

    def install(self, catalog_id):
        """Install the specified catalog.

        Parameters
        ----------
        catalog_id : str
            The ID of the catalog - format /api/v1/catalog/[0-9]+

        Raises
        -------
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
        -------
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


class Catalog:
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

    def __init__(self, json):
        """Create a Catalog Image.

        Parameters
        ----------
        json : str
            The json returned by the API representing a Catalog.

        Returns
        -------
        Catalog:
            An instance of Catalog

        Note
        ----
        Users of the library aren't expected to create instances of this class
        directly.
        """
        self.json = json
        self.display_columns = Catalog.default_display_fields

    def __repr__(self):
        return "<Catalog id:{} state:{}>".format(self.id, self.state)

    def __str__(self):
        return "Catalog(distro_id={}, state={})".format(
            self.distro_id, self.state
        )

    def __dir__(self):
        return self.display_columns

    def __getitem__(self, item):
        return getattr(self, self.display_columns[item])

    def __len__(self):
        return len(dir(self))

    def set_display_columns(self, columns):
        """Set the columns this instance should have when the instance is used

        with :py:meth:`.CatalogList.tabulate`.

        Parameters
        ----------
        columns : list[str]
            Set the list of colums to return

        See Also
        --------
        See :py:attr:`all_fields` for the complete list of field names.
        """
        self.display_columns = columns

    @property
    def id(self):
        """@Field: from json['_links']['self']['href'] -

        id format: '/api/v1/catalog/[0-9]+'
        """
        return self.json["_links"]["self"]["href"]

    @property
    def distro_id(self):
        """@Field: from json['distro_id']"""
        return self.json["distro_id"]

    @property
    def state(self):
        """@Field: from json['state']"""
        return self.json["state"]


class CatalogList:
    """List of :py:obj:`.Catalog` objects.

    Parameters
    ----------
    json : str
        json data returned from the HPE Container Platform API get request
        to /api/v1/catalog

    Note
    ----
    This class is not expected to be instantiated by users.
    """

    def __init__(self, json):
        self.json = json
        self.catalogs = sorted(
            [Catalog(g) for g in json], key=attrgetter("id"),
        )
        self.display_columns = Catalog.default_display_fields

    def __getitem__(self, item):
        return self.catalogs[item]

    # Python 2
    def next(self):
        """Support iterator access on Python 2.7."""
        if not self.catalogs:
            raise StopIteration
        catalog = self.catalogs.pop(0)
        catalog.set_display_columns(self.display_columns)
        return catalog

    # Python 3
    def __next__(self):
        if not self.catalogs:
            raise StopIteration
        catalog = self.catalogs.pop(0)
        catalog.set_display_columns(self.display_columns)
        return catalog

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.catalogs)

    def tabulate(
        self,
        columns=Catalog.default_display_fields,
        style="pretty",
        display_headers=True,
    ):
        """Provide a tabular represenation of the list of Catalog images.

        Parameters
        ----------
        columns : list[str]
            list of columns to return in the table - default
            :py:attr:`.Catalog.default_display_fields`
        style: str
            See: https://github.com/astanin/python-tabulate#table-format

        Returns
        -------
        str
            table output

        Example
        -------
        Print the catalog list with all of the avaialble fields:

        >>> print(hpeclient.catalog.list().tabulate())

        Print the cluster list with a subset of the fields:

        >>> print(hpeclient.catalog.list().tabulate(columns=['id', 'state']))
        """
        if columns != Catalog.default_display_fields:
            assert isinstance(
                columns, list
            ), "'columns' parameter must be list"
            for column in columns:
                assert (
                    column in Catalog.all_fields
                ), "item %s is not a field in Catalog.all_fields" % (column)

        self.display_columns = columns

        # FIXME:
        # https://github.com/hpe-container-platform-community/hpecp-python-library/issues/5
        if display_headers:
            return tabulate(self, headers=columns, tablefmt=style)
        else:
            return tabulate(self, tablefmt=style)
