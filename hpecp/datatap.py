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
        "label_name",
        "label_description",
        "self_href",
        # "state",
        # "state_info",
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
        """@Field: from json['label']['name']."""
        try:
            return self.json["label"]["name"]
        except KeyError:
            return ""

    @property
    def label_description(self):
        """@Field: from json['label']['description']."""
        try:
            return self.json["label"]["description"]
        except KeyError:
            return ""

    @property
    def self_href(self):
        """@Field: from json['_links']['self']['href']."""
        try:
            return self.json["_links"]["self"]["href"]
        except KeyError:
            return ""

    # @property
    # def state(self):
    #     """@Field: from json['state']"""
    #     try:
    #         return self.json["state"]
    #     except KeyError:
    #         return ""

    # @property
    # def state_info(self):
    #     """@Field: from json['state_info']"""
    #     try:
    #         return self.json["state_info"]
    #     except KeyError:
    #         return ""


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
        service_id,
        backup_host,
        endpoint_type,
        endpoint_port,
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
        service_id : [type]
            [description]
        backup_host : [type]
            [description]
        endpoint_type : [type]
            [description]
        endpoint_port : [type]
            [description]
        read_only : [type]
            [description]
        """
        _data = {
            "bdfs_root": {"path_from_endpoint": path_from_endpoint},
            "endpoint": {
                "kdc_data": [{"host": kdc_data_host, "port": kdc_data_port}],
                "realm": realm,
                "client_principal": client_principal,
                "browse_only": browse_only,
                "host": host,
                "keytab": keytab,
                "service_id": service_id,
                "backup_host": backup_host,
                "type": endpoint_type,
                "port": endpoint_port,
            },
            "flags": {"read_only": read_only},
            "label": {"name": name, "description": description},
        }

        self.client._request(
            url=DatatapController.base_resource_path,
            http_method="post",
            description="datatap/create",
            data=_data,
        )
