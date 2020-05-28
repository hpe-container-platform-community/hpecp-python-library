from __future__ import absolute_import

# from .logger import Logger
# from .exceptions import ContainerPlatformClientException, APIException, APIItemNotFoundException, APIItemConflictException

import json
import re

try:
    basestring
except NameError:
    basestring = str


class UserController:
    """
    The methods of this class can be invoked using `client.user.method()`.  See the example below:

    Example::

        client = ContainerPlatformClient(...).create_session()
        client.user.create()

    """

    def __init__(self, client):
        self.client = client

    def create(self, name, description="", is_external=True):
        """Create a user by specifying name & description

        Args:
            name: str
                Client name.
            description: str
                Description as a string.
            is_external: bool
                Set to True for external users

        Returns: user ID
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
        return response.headers["location"]
