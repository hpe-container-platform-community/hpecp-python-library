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

"""Module for working with datatap."""

from .base_resource import AbstractResource, AbstractResourceController


class Datatap(AbstractResource):
    """Datatap Image item."""

    # All of the fields of Catalog objects as returned by the HPE Container
    # Platform API.
    # TODO: Verify this with the specification
    all_fields = (
        "id",
        "name",
        "description",
        "type",
        "status",
    )

    default_display_fields = [
        "id",
        "name",
        "description",
        "type",
        "status",
    ]

    # These fields are displayed by default, e.g. in tabulate()
    # TODO: Verify this with the specification
    # TODO: Pick a smaller subset, again based on the API response
    default_display_fields = all_fields

    @property
    def name(self):
        """@Field: from json['_embedded']['label']['name']."""
        try:
            return self.json["_embedded"]["label"]["name"]
        except KeyError:
            return ""

    @property
    def description(self):
        """@Field: from json['_embedded']['label']['description']."""
        try:
            return self.json["_embedded"]["label"]["description"]
        except KeyError:
            return ""

    @property
    def type(self):
        """@Field: from json['_embedded']['endpoint']['type']."""
        try:
            return self.json["_embedded"]["endpoint"]["type"]
        except KeyError:
            return ""

    @property
    def self_href(self):
        """@Field: from json['_links']['self']['href']."""
        try:
            return self.json["_links"]["self"]["href"]
        except KeyError:
            return ""

    @property
    def status(self):
        """@Field: from json['_embedded']['status']."""
        try:
            return self.json["_embedded"]["status"]
        except KeyError:
            return ""


class DatatapController(AbstractResourceController):
    """Class that users will interact with to work with datataps.

    An instance of this class is available in the
    `client.ContainerPlatformClient` with the attribute name
    :py:attr:`datatap <.client.ContainerPlatformClient.catalog>`. The methods
    of this class can be invoked using `client.datatap.method()`. See the
    example below:

    Examples
    --------
    >>> client = ContainerPlatformClient(...).create_session()
    >>> client.datatap.list()
    """

    base_resource_path = "/api/v1/dataconn"

    resource_list_path = "data_connectors"

    resource_class = Datatap

    def create_hdfs_with_kerberos(
        self,
        name,
        description,
        path_from_endpoint,
        kdc_data_host,
        kdc_data_port,
        realm,
        client_principal,
        browse_only,
        host,
        keytab,
        backup_host,
        type,
        port,
        read_only,
    ):
        """TODO.

        Parameters
        ----------
        name : [type]
            [description]
        description : [type]
            [description]
        path_from_endpoint : [type]
            [description]
        kdc_data_host : [type]
            [description]
        kdc_data_port : [type]
            [description]
        realm : [type]
            [description]
        client_principal : [type]
            [description]
        browse_only : [type]
            [description]
        host : [type]
            [description]
        keytab : [type]
            [description]
        backup_host : [type]
            [description]
        type : [type]
            [description]
        port : [type]
            [description]
        read_only : [type]
            [description]
        """
        _data = {
            "bdfs_root": {},
            "endpoint": {
                "kdc_data": [
                    {
                        "host": kdc_data_host,
                    }
                ],
                "realm": realm,
                "client_principal": client_principal,
                "browse_only": browse_only,
                "host": host,
                "keytab": keytab,
                "service_id": "hdfs",
                "backup_host": backup_host,
                "type": type,
                "port": str(port),
            },
            "flags": {"read_only": read_only},
            "label": {"name": name, "description": description},
        }

        if path_from_endpoint != "":
            _data["bdfs_root"]["path_from_endpoint"] = path_from_endpoint

        if kdc_data_port != "":
            _data["endpoint"]["kdc_data"]["kdc_data_port"] = kdc_data_port

        self.client._request(
            url=DatatapController.base_resource_path,
            http_method="post",
            description="datatap/create",
            data=_data,
        )
