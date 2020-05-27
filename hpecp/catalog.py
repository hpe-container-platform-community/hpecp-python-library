from operator import attrgetter

from tabulate import tabulate


class CatalogController:
    """This is the main class that users will interact with to talk to catalogs.

    An instance of this class is available in the
    `client.ContainerPlatformClient` with the attribute name
    :py:attr:`catalog <.client.ContainerPlatformClient.catalog>`. The methods
    of this class can be invoked using `client.catalog.method()`. See the
    example below:

    Example:

        client = ContainerPlatformClient(...).create_session()
        client.catalog.list()

    """

    def __init__(self, client):
        self.client = client

    def list(self):
        """Retrieve a list of Catalogs

        Returns:
            CatalogList: list of Catalogs

        Raises:
            APIException
        """
        response = self.client._request(
            url="/api/v1/catalog/",
            http_method="get",
            description="catalog/list"
        )
        return CatalogList(
            response.json()["_embedded"]["independent_catalog_entries"])


class Catalog:
    """Create an instance of Catalog from json data returned from the HPE

    Container Platform API. Users of this library are not expected to create an
    instance of this class.

    Parameters:
        json : str
            The json returned by the API representing a Catalog.

    Returns:
        Catalog:
            An instance of Catalog
    """

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
        "state_info"
    )

    # These fields are displayed by default, e.g. in tabulate()
    # TODO: Verify this with the specification
    # TODO: Pick a smaller subset, again based on the API response
    default_display_fields = all_fields

    def __init__(self, json):
        self.json = json
        self.display_columns = Catalog.default_display_fields

    # def __repr__(self):
    #     return "<Catalog id:{} state:{}>".format(self.id, self.state)

    # def __str__(self):
    #     return "K8sCluster(id={}, state={})".format(self.id, self.state)

    def __dir__(self):
        return self.display_columns

    def __getitem__(self, item):
        return getattr(self, self.display_columns[item])

    def __len__(self):
        return len(dir(self))

    def set_display_columns(self, columns):
        """Set the columns this instance should have when the instance is used

        with :py:meth:`.CatalogList.tabulate`.

        Parameters:
            columns : list[str]
                Set the list of colums to return

        See :py:attr:`all_fields` for the complete list of field names.
        """
        self.display_columns = columns


class CatalogList:
    """List of :py:obj:`.Catalog` objects

    This class is not expected to be instantiated by users.

    Parameters:
        json : str
            json data returned from the HPE Container Platform API get request
            to /api/v1/catalog
    """

    def __init__(self, json):
        self.json = [g for g in json if g["purpose"] == "proxy"]
        self.catalogs = sorted(
            [Catalog(g) for g in json
             if g["purpose"] == "proxy"], key=attrgetter("id")
        )
        self.display_columns = Catalog.default_display_fields

    def __getitem__(self, item):
        return self.catalogs[item]

    # Python 2
    def next(self):
        """Support iterator access on Python 2.7"""
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
        """Provide a tabular represenation of the list of Catalogs

        Parameters:
            columns : list[str]
                list of columns to return in the table - default
                :py:attr:`.Catalog.default_display_fields`
            style: str
                See: https://github.com/astanin/python-tabulate#table-format

        Returns:
            str : table output

        Example::

            # Print the catalog list with all of the avaialble fields
            print(hpeclient.catalog.list().tabulate())

            # Print the cluster list with a subset of the fields
            print(hpeclient.catalog.list().tabulate(columns=['id', 'state']))
        """
        if columns != Catalog.default_display_fields:
            assert isinstance(columns, list),\
                "'columns' parameter must be list"
            for column in columns:
                assert (
                    column in Catalog.all_fields
                ), f"item '{column}' is not a field in Catalog.all_fields"

        self.display_columns = columns

        # FIXME: https://github.com/hpe-container-platform-community/hpecp-python-library/issues/5
        if display_headers:
            return tabulate(self, headers=columns, tablefmt=style)
        else:
            return tabulate(self, tablefmt=style)
