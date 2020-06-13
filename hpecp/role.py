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

import json
import re

from .exceptions import APIItemNotFoundException

try:
    basestring
except NameError:
    basestring = str


class RoleController:
    """This is the main class that users will interact with to work with roles.

    An instance of this class is available in the client.ContainerPlatformClient with the attribute name
    :py:attr:`role <.client.ContainerPlatformClient.role>`.  The methods of this class can be
    invoked using `client.role.method()`.  See the example below:

    Example::

        client = ContainerPlatformClient(...).create_session()
        client.role.get()

    """

    def __init__(self, client):
        self.client = client

    def get(self, role_id):
        """Retrieve a Role by ID.

        Args:
            role_id: str
                The role ID - format: '/api/v1/role/[0-9]+'

        Returns:
            Role: object representing Role

        Raises:
            APIException
        """
        assert isinstance(
            role_id, str
        ), "'role_id' must be provided and must be a string"
        assert re.match(
            r"\/api\/v1\/role\/[0-9]+", role_id
        ), "'role_id' must have format '/api/v1/role/[0-9]+'"

        response = self.client._request(
            url=role_id, http_method="get", description="role/get"
        )

        return Role(response.json())


class Role:
    """Create an instance of Role from json data returned from the HPE Container Platform API.

    Users of this library are not expected to create an instance of this class.

    Parameters:
        json : str
            The json returned by the API representing a Gateway.

    Returns:
        Gateway:
            An instance of Gateway
    """

    all_fields = [
        "id",
        "name",
        "description",
    ]
    """All of the fields of Role objects as returned by the HPE Container Platform API"""

    default_display_fields = [
        "id",
        "name",
        "description",
    ]
    """These fields are displayed by default, e.g. in tabulate()"""

    def __init__(self, json):
        self.json = json
        self.display_columns = Role.default_display_fields

    def __repr__(self):
        return "<Role id:{} description:{}>".format(self.id, self.description)

    def __str__(self):
        return "Role(id={}, description={})".format(self.id, self.description)

    def __dir__(self):
        return self.display_columns

    def __getitem__(self, item):
        return getattr(self, self.display_columns[item])

    def __len__(self):
        return len(dir(self))

    @property
    def id(self):
        """@Field: from json['_links']['self']['href'] - id format: '/api/v1/role/[0-9]+'"""
        return self.json["_links"]["self"]["href"]

    @property
    def name(self):
        """@Field: from json['label']['name']"""
        return self.json["label"]["name"]

    @property
    def description(self):
        """@Field: from json['label']['description']"""
        return self.json["label"]["description"]
