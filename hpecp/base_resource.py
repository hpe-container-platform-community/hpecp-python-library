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

"""Base classes for Controllers and Resources."""

import abc
import urllib

import polling
import six
from tabulate import tabulate

from hpecp.exceptions import APIItemNotFoundException

from .logger import Logger

_log = Logger.get_logger()


@six.add_metaclass(abc.ABCMeta)
class AbstractResourceController:
    """Base class for Resource Controllers."""

    def _get_base_resource_path(self):
        return self._base_resource_path

    def _set_base_resource_path(self, path):
        assert (
            path.endswith("/") is False
        ), "base resource path must not end with '/'"
        self._base_resource_path = path

    base_resource_path = abc.abstractproperty(
        _get_base_resource_path, _set_base_resource_path
    )
    """Declare the resource base path for the API resource.

    :getter: Returns the resource base path
    :setter: Sets the resource base path
    :type: str

    Example
    -------
    class K8sClusterController(AbstractResourceController):
        ...
        base_resource_path = "/api/v2/k8scluster"
    """

    def _get_resource_class(self):
        return self._resource_class

    def _set_resource_class(self, clazz):
        self._resource_class = clazz

    resource_class = abc.abstractproperty(
        _get_resource_class, _set_resource_class
    )
    """Declare the implementing Resource class for the API resource.
    The resource class contains properties mapping to attributes in the
    response.

    :getter: Returns the Resource class
    :setter: Sets the Resource class
    :type: class

    Example
    -------
    class K8sClusterController(AbstractResourceController):
        ...
        resource_class = K8sCluster
    """

    def _get_resource_list_path(self):
        return self._resource_list_path

    def _set_resource_list_path(self, resource_list_path):
        self._resource_list_path = resource_list_path

    resource_list_path = abc.abstractproperty(
        _get_resource_list_path, _set_resource_list_path
    )
    """Declare the implementing resource list path for the API resource.
    The resource list path is where the resources are after the
    '_embedded' element in the API response json.

    :getter: Returns the resource list path
    :setter: Sets the resource list path
    :type: str

    Example
    -------
    class K8sClusterController(AbstractResourceController):
        ...
        resource_list_path = "k8sclusters"
    """

    def __init__(self, client):
        """Create a new instance.

        Parameters
        ----------
        client : ContainerPlatformClient
            client instance for working with the HPE CP API.
        """
        self.client = client

    def get(self, id, params={}):
        """Make an API call to retrieve a Resource.

        Parameters
        ----------
        id : str
            The ID with the format /resource/path/id
        params : str, optional
            API Parameters.

        Returns
        -------
        Instance of self.resource_class
            An instance of the class defined by the property
            self.resource_class

        Raises
        ------
        APIException
            The remote API returned an error.
        APIItemNotFoundException
            The item with {id} was not found.
        """
        assert isinstance(id, str), "'id' must be provided and must be a str"
        assert id.startswith(
            self.base_resource_path
        ), "'id' does not start with '{}'".format(self.base_resource_path)

        if params:
            if six.PY2:
                p = "?" + urllib.urlencode(params)
            else:
                p = "?" + urllib.parse.urlencode(params)
        else:
            p = ""

        response = self.client._request(
            url="{}{}".format(id, p),
            http_method="get",
            description=self.__class__.__name__ + "/get",
        )
        return self.resource_class(response.json())

    def list(self):
        """Make an API call to retrieve a list of Resources.

        Returns
        -------
        ResourceList
            The ResourceList will contain instances of the class defined by
            the property self.resource_class
        """
        response = self.client._request(
            url=self.base_resource_path,
            http_method="get",
            description=self.__class__.__name__ + "/list",
        )
        return ResourceList(
            self.resource_class,
            response.json()["_embedded"][self.resource_list_path],
        )

    def delete(self, id):
        """Make an API call to delete a Resources.

        Parameters
        ----------
        id : str
            The ID with the format /resource/path/id

        Raises
        ------
        APIException
            The remote API returned an error.
        APIItemNotFoundException
            The item with {id} was not found.
        """
        assert isinstance(id, str), "'id' must be provided and must be a str"
        assert id.startswith(
            self.base_resource_path
        ), "'id' does not start with '{}'".format(self.base_resource_path)

        self.client._request(
            url=id,
            http_method="delete",
            description=self.__class__.__name__ + "/delete",
        )


@six.add_metaclass(abc.ABCMeta)
class AbstractWaitableResourceController(AbstractResourceController):
    """Resource Controller that is able to wait for the resource's status."""

    def _get_status_class(self):
        return self._status_class

    def _set_status_class(self, clazz):
        self._status_class = clazz

    status_class = abc.abstractproperty(_get_status_class, _set_status_class)
    """Declare the implementing Status class for the API resource.
    The status class contains properties mapping to attributes in the
    response.

    :getter: Returns the Status class
    :setter: Sets the Status class
    :type: class

    Example
    -------
    class K8sClusterController(AbstractResourceController):
        ...
        status_class = K8sClusterStatus
    """

    def _get_status_fieldname(self):
        return self._status_fieldname

    def _set_status_fieldname(self, fieldname):
        self._status_fieldname = fieldname

    status_fieldname = abc.abstractproperty(
        _get_status_fieldname, _set_status_fieldname
    )
    """Declare the Status fieldname in the API resource.

    Usually either: status or state

    :getter: Returns the Status fieldname
    :setter: Sets the Status fieldname
    :type: str

    Example
    -------
    class K8sClusterController(AbstractResourceController):
        ...
        status_fieldname = status
    """

    def wait_for_state(self, id, states=[], timeout_secs=1200):
        """See wait_for_status()."""
        return self.wait_for_status(id, states, timeout_secs)

    def wait_for_status(self, id, status=[], timeout_secs=1200):
        """Wait for K8S worker status.

        Parameters
        ----------
        id: str
            The resource ID - format: '/resource/path/[0-9]+'
        status: list[:py:method:`status_class`]
            Status(es) to wait for.  Use an empty array if you want to
            wait for the resource existence to cease.
        timeout_secs: int
            How long to wait for the status(es) before raising an
            exception.

        Returns
        -------
        bool
            True if status was found before timeout, otherwise False
            True if item does not exist before timeout and status is empty
        """
        assert isinstance(status, list), "'status' must be a list"
        for i, s in enumerate(status):
            assert isinstance(
                s, self.status_class
            ), "'status' item '{}' is not of type {}".format(
                i, self.status_class
            )
        assert isinstance(timeout_secs, int), "'timeout_secs' must be an int"
        assert timeout_secs >= 0, "'timeout_secs' must be >= 0"

        # if status is empty return success when resource id not found
        if len(status) == 0:
            _log.debug(
                "waiting {}s for item {} to cease existence".format(
                    timeout_secs, id
                )
            )

            def item_not_exists():
                try:
                    self.get(id)
                    return False
                except APIItemNotFoundException:
                    return True

            try:
                polling.poll(
                    lambda: item_not_exists(),
                    step=10,
                    poll_forever=False,
                    timeout=timeout_secs,
                )
                return True
            except polling.TimeoutException:
                return False

        # if state is not empty return success when resource current state is
        # in desired state
        else:
            waiting_for_status = [s.name for s in status]

            _log.debug(
                "waiting {}s for item {} to have status in {}".format(
                    timeout_secs, id, waiting_for_status
                )
            )
            try:

                def get_status():
                    status = getattr(self.get(id), self.status_fieldname)
                    return status

                polling.poll(
                    lambda: (get_status() in waiting_for_status),
                    step=10,
                    poll_forever=False,
                    timeout=timeout_secs,
                )
                _log.debug(
                    "Found item {} with status in {}".format(
                        id, waiting_for_status
                    )
                )
                return True
            except polling.TimeoutException:
                _log.debug(
                    "Timed out waiting for {} to have status in {}".format(
                        id, waiting_for_status
                    )
                )
                return False


@six.add_metaclass(abc.ABCMeta)
class AbstractResource:
    """Base class for Resource class repreenting an API resource.

    The resource class contains properties mapping to attributes in the
    response.

    The implementing class is declared in the ResourceController:

    Example
    -------
    class K8sClusterController(AbstractResourceController):
        ...
        resource_class = K8sCluster
    """

    def _get_all_fields(self):
        return self.all_fields

    def _set_all_fields(self, fields):
        self.all_fields = fields

    all_fields = abc.abstractproperty(_get_all_fields, _set_all_fields)

    def __init__(self, json):
        """Create a new Resource class.

        Parameters
        ----------
        json : obj
            JSON returned from the API for the Resource.
        """
        self.json = json

    def __repr__(self):
        """Return a represenation of Resource class."""
        return "<{} id:{}>".format(self.__class__.__name__, self.id)

    def __str__(self):
        """Return a str representation of a Resource class."""
        return "{}(id={})".format(self.__class__.__name__, self.id)

    @property
    def id(self):
        """@Field: from json['_links']['self']['href']."""
        return self.json["_links"]["self"]["href"]

    @property
    def _links(self):
        """@Field: from json['_links']."""
        return self.json["_links"]

    def __len__(self):
        """Return the number of resource fields in the Resource class."""
        return len(dir(self))


class ResourceList:
    """List of Resource objects."""

    def __init__(self, resource_class, json):
        """Create a list of resources using the resource_class.

        Parameters
        ----------
        resource_class : class
            Resource implementation class
        json : obj
            JSON return from the API
        """
        self.json = json
        self.resource_class = resource_class
        self.resources = [self.resource_class(j) for j in json]

    def __getitem__(self, item):
        """Retrieve a field value."""
        return self.resources[item]

    def tabulate(self, columns=[], style="pretty", display_headers=True):
        """Return a tabule output of the ResourceList.

        Parameters
        ----------
        columns : list, optional
            List of columns to output. The default value of an empty list
            will output all the available fields
        style : str, optional
            Table styles, by default "pretty"

            The available styles are:

            "plain"
            "simple"
            "github"
            "grid"
            "fancy_grid"
            "pipe"
            "orgtbl"
            "jira"
            "presto"
            "pretty"
            "psql"
            "rst"
            "mediawiki"
            "moinmoin"
            "youtrack"
            "html"
            "latex"
            "latex_raw"
            "latex_booktabs"
            "textile"

            See section 'Table Format' in https://pypi.org/project/tabulate/
            for more information

        Returns
        -------
        str
            table output of Resource

        Example
        -------
        Print the cluster list with all of the avaialble fields
        >>> print(hpeclient.cluster.list().tabulate())

        Print the cluster list with a subset of the fields
        >>> print(hpeclient.cluster.list().tabulate(
        ...     columns=['id', 'name','description']))
        """
        assert isinstance(columns, list), "'columns' parameter must be list"

        if len(columns) == 0:
            columns = self.resource_class.all_fields

        for field in columns:
            assert (
                field in self.resource_class.all_fields
            ), "item '{}' is not a field in {}.all_fields".format(
                field, self.__class__.__name__
            )

        self.display_fields = columns

        table = []
        for resource in self.resources:
            row = []
            for col in columns:
                if not hasattr(resource, col):
                    _log.warn(
                        "Field {} not found in {} - json {}".format(
                            col, resource, self.json
                        )
                    )
                row.append(getattr(resource, col, ""))
            table.append(row)

        if display_headers:
            output = tabulate(table, headers=columns, tablefmt=style)
        else:
            output = tabulate(table, tablefmt=style)

        if six.PY2:
            return output.encode(encoding="UTF-8", errors="strict")
        else:
            return output
