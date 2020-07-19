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
from operator import attrgetter

from tabulate import tabulate

from .exceptions import APIItemNotFoundException
from requests.structures import CaseInsensitiveDict

try:
    basestring
except NameError:
    basestring = str


class UserController:
    """Class that users will interact with to work with catalogs.

    An instance of this class is available in the
    client.ContainerPlatformClient with the attribute name
    :py:attr:`user <.client.ContainerPlatformClient.user>`.  The methods of
    this class can be invoked using `client.user.method()`.  See the example
    below:

    Example
    -------
    >>> client = ContainerPlatformClient(...).create_session()
    >>> client.user.list()
    """

    def __init__(self, client):
        self.client = client

    def list(self):
        """Retrieve a list of Users.

        Returns
        -------
        UserList
            list of Users

        Raises
        ------
        APIException
        """
        response = self.client._request(
            url="/api/v1/user/", http_method="get", description="user/list"
        )
        return UserList(response.json()["_embedded"]["users"])

    def get(self, user_id):
        """Retrieve a User by ID.

        Parameters
        ----------
        user_id: str
            The user ID - format: '/api/v1/user/[0-9]+'

        Returns
        -------
        User
            object representing a User

        Raises
        ------
        APIException
        """
        assert isinstance(
            user_id, str
        ), "'user_id' must be provided and must be a string"
        assert re.match(
            r"\/api\/v1\/user\/[0-9]+", user_id
        ), "'user_id' must have format '/api/v1/user/[0-9]+'"

        response = self.client._request(
            url=user_id, http_method="get", description="user/get"
        )
        if response.json()["purpose"] != "proxy":
            raise APIItemNotFoundException(
                message="user not found with id: " + user_id,
                request_method="get",
                request_url=user_id,
            )

        return User(response.json())

    def delete(self, user_id):
        """Delete a user.

        Parameters
        ----------
        user_id: str
            The User ID - format: '/api/v1/user/[0-9]+'

        Raises
        ------
        APIException
        """
        assert isinstance(
            user_id, str
        ), "'user_id' must be provided and must be a string"
        assert re.match(
            r"\/api\/v1\/user\/[0-9]+", user_id
        ), "'user_id' must have format '/api/v1/user/[0-9]+'"

        # Check if host is actually a user
        # Raises APIItemNotFoundException() if user not found
        self.get(user_id)

        self.client._request(
            url=user_id, http_method="delete", description="user/delete"
        )

    def wait_for_delete(self, user_id, timeout_secs=1200):
        """Not Implemented yet"""
        raise NotImplementedError()

    def create(self, name, description="", is_external=True):
        """Create a user by specifying name and description.

        Parameters
        ----------
        name: str
            Client name.
        description: str
            Description as a string.
        is_external: bool
            Set to True for external users

        Returns
        -------
        str
            The user ID
        """

        assert isinstance(
            name, basestring
        ), "'name' must be provided and must be a string"
        assert isinstance(
            description, basestring
        ), "'description must be a string"
        assert isinstance(
            is_external, bool
        ), "'is_external' must be provided and must be a bool"

        data = {
            "label": {"name": name, "description": description},
            "is_external": is_external,
        }

        response = self.client._request(
            url="/api/v1/user",
            http_method="post",
            data=data,
            description="user/create",
        )
        return CaseInsensitiveDict(response.headers)["location"]


class User:
    """Create an instance of User from json data returned from the HPE
    Container Platform API. Users of this library are not expected to create an
    instance of this class.

    Parameters
    ----------
    json : str
        The json returned by the API representing a User.

    Returns
    -------
    User
        An instance of User
    """

    all_fields = [
        "label",
        "is_group_added_user",
        "is_external",
        "is_service_account",
        "default_tenant",
        "is_siteadmin",
    ]
    # All of the fields of User objects as returned by the HPE Container
    # Platform API

    default_display_fields = ["label", "is_service_account", "is_siteadmin"]
    """These fields are displayed by default, e.g. in tabulate()"""

    def __init__(self, json):
        self.json = json
        self.display_columns = User.default_display_fields

    def set_display_columns(self, columns):
        """Set the columns this instance should have when the instance is
        used with :py:meth:`.User.tabulate`

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

        id format: '/api/v1/user/[0-9]+'
        """
        return self.json["_links"]["self"]["href"]

    @property
    def label(self):
        """@Field: from json['label']"""
        return self.json["label"]

    @property
    def is_group_added_user(self):
        """@Field: from json['is_group_added_user']"""
        return self.json["is_group_added_user"]

    @property
    def is_external(self):
        """@Field: from json['is_external']"""
        return self.json["is_external"]

    @property
    def is_service_account(self):
        """@Field: from json['is_service_account']"""
        return self.json["is_service_account"]

    @property
    def default_tenant(self):
        """@Field: from json['default_tenant']"""
        return self.json["default_tenant"]

    @property
    def is_siteadmin(self):
        """@Field: from json['is_siteadmin']"""
        return self.json["is_siteadmin"]

    @property
    def _links(self):
        """@Field: from json['_links']"""
        return self.json["_links"]


class UserList:
    """List of :py:obj:`.User` objects."""

    def __init__(self, json):
        """Create a UserList object.
        This class is not expected to be instantiated by users.

        Parameters
        ----------
        json : str
            json data returned from the HPE Container Platform API get request
            to /api/v1/user
        """
        self.json = json
        self.users = sorted([User(g) for g in json], key=attrgetter("id"))
        self.display_columns = User.default_display_fields

    def __getitem__(self, item):
        return self.users[item]

    # Python 2
    def next(self):
        """Support iterator access on Python 2.7"""
        if not self.users:
            raise StopIteration
        user = self.users.pop(0)
        user.set_display_columns(self.display_columns)
        return user

    # Python 3
    def __next__(self):
        if not self.users:
            raise StopIteration
        user = self.users.pop(0)
        user.set_display_columns(self.display_columns)
        return user

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.users)

    def tabulate(
        self,
        columns=User.default_display_fields,
        style="pretty",
        display_headers=True,
    ):
        """Provide a tabular represenation of the list of Users.

        Parameters
        ----------
        columns : list[str]
            list of columns to return in the table - default
            :py:attr:`.User.default_display_fields`
        style: str
            See: https://github.com/astanin/python-tabulate#table-format

        Returns
        -------
        str
            table output of Users

        Example
        -------
        Print the user list with all of the avaialble fields
        >>> print(hpeclient.user.list().tabulate())

        Print the cluster list with a subset of the fields
        >>> print(hpeclient.user.list().tabulate(columns=['id', 'state']))
        """
        if columns != User.default_display_fields:
            assert isinstance(
                columns, list
            ), "'columns' parameter must be list"
            for column in columns:
                assert (
                    column in User.all_fields
                ), "item '{}' is not a field in User.all_fields".format(column)

        self.display_columns = columns

        if display_headers:
            return tabulate(self, headers=columns, tablefmt=style)
        else:
            return tabulate(self, tablefmt=style)
