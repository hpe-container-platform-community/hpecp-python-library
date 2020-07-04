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

import abc, six

import re

from operator import attrgetter

from tabulate import tabulate

from .logger import Logger


@six.add_metaclass(abc.ABCMeta)
class AbstractResourceController:
    def _get_base_resource_path(self):
        return self._resource_path

    def _set_base_resource_path(self, path):
        """E.g.  /api/v2/k8scluster"""
        self._base_resource_path = path

    base_resource_path = abc.abstractproperty(
        _get_base_resource_path, _set_base_resource_path
    )

    def _get_resource_class(self):
        return self._resource_class

    def _set_resource_class(self, clazz):
        self._resource_class = clazz

    resource_class = abc.abstractproperty(
        _get_resource_class, _set_resource_class
    )

    # def _get_resource_list_class(self):
    #     return self._resource_list_class

    # def _set_resource_list_class(self, clazz):
    #     self._resource_list_class = clazz

    # resource_list_class = abc.abstractproperty(
    #     _get_resource_list_class, _set_resource_list_class
    # )

    @abc.abstractmethod
    def get(self, id, params):

        assert isinstance(id, str), "'id' must be provided and must be a str"
        assert id.startswith(
            self.base_resource_path
        ), "'id' does not start with '{}'".format(self.base_resource_path)

        response = self.client._request(
            url="{}{}".format(id, params),
            http_method="get",
            description=self.__class__.__name__ + "/get",
        )
        return self.resource_class(response.json())

    @abc.abstractmethod
    def list(self):

        response = self.client._request(
            url=self.base_resource_path,
            http_method="get",
            description=self.__class__.__name__ + "/list",
        )
        return ResourceList(
            self.resource_class, response.json()["_embedded"]["k8sclusters"]
        )

    @abc.abstractmethod
    def delete(self, id):
        """
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
class AbstractResource:
    def _get_all_fields(self):
        return self.all_fields

    def _set_all_fields(self, fields):
        self.all_fields = fields

    all_fields = abc.abstractproperty(_get_all_fields, _set_all_fields)

    # def get_display_fields(self):
    #     return list(self.display_fields)

    # def set_display_fields(self, display_fields):
    #     self.display_fields = list(display_fields)

    def __init__(self, json):
        self.json = json
        # self.set_display_fields(self.__class__.all_fields)

    def __repr__(self):
        return "<{} id:{}>".format(self.__class__.__name__, self.id)

    def __str__(self):
        return "K8sCluster(id={})".format(self.__class__.__name__.self.id)

    # def __dir__(self):
    #     return self.display_fields

    # def __getitem__(self, item):
    #     prop = getattr(self, self.get_display_fields[item])
    #     return prop

    # def set_display_fields(self, fields):
    #     self.display_fields = fields

    @property
    def id(self):
        """@Field: from json['_links']['self']['href']"""
        return self.json["_links"]["self"]["href"]

    @property
    def _links(self):
        """@Field: from json['_links']"""
        return self.json["_links"]

    def __len__(self):
        return len(dir(self))


class ResourceList:
    def __init__(self, resource_class, json):
        self.json = json
        self.resource_class = resource_class
        self.resources = [self.resource_class(j) for j in json]
        # self.display_fields = list(resource_class.all_fields)

    # # Python 2
    # def next(self):
    #     """Support iterator access on Python 2.7"""
    #     if not self.resource:
    #         raise StopIteration
    #     resource = self.resource.pop(0)
    #     resource.set_display_fields(self.display_fields)
    #     return resource

    # # Python 3
    # def __next__(self):
    #     if not self.resource:
    #         raise StopIteration
    #     resource = self.resource.pop(0)
    #     resource.set_display_fields(self.display_fields)
    #     return resource

    # def __iter__(self):
    #     return self

    # def __len__(self):
    #     return len(self.resource)

    def __getitem__(self, item):
        return self.resources[item]

    def tabulate(self, columns=[], style="pretty"):
        """
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
                row.append(getattr(resource, col))
            table.append(row)
                
            
        return tabulate(table, headers=columns, tablefmt=style)
