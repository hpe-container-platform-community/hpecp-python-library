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

import re

from .base_resource import AbstractResource, AbstractResourceController

try:
    basestring
except NameError:
    basestring = str


class Role(AbstractResource):
    """Create an instance of Role from json data returned from the HPE
    Container Platform API.

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
    """All of the fields of Role objects as returned by the HPE Container
    Platform API"""

    default_display_fields = [
        "id",
        "name",
        "description",
    ]

    @property
    def id(self):
        """@Field: from json['_links']['self']['href'] - id format:
        '/api/v1/role/[0-9]+'"""
        return self.json["_links"]["self"]["href"]

    @property
    def name(self):
        """@Field: from json['label']['name']"""
        return self.json["label"]["name"]

    @property
    def description(self):
        """@Field: from json['label']['description']"""
        return self.json["label"]["description"]


class RoleController(AbstractResourceController):
    """This is the main class that users will interact with to work with roles.

    An instance of this class is available in the
    client.ContainerPlatformClient with the attribute name
    :py:attr:`role <.client.ContainerPlatformClient.role>`.  The methods of
    this class can be
    invoked using `client.role.method()`.  See the example below:

    Example::

        client = ContainerPlatformClient(...).create_session()
        client.role.get()

    """

    base_resource_path = "/api/v1/role/"
    resource_class = Role
    resource_list_path = "roles"
