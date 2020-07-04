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

    all_fields = abc.abstractproperty(
        _get_all_fields, _set_all_fields
    )

    def __init__(self, json):
        self.json = json
        self.display_columns = self.__class__.all_fields

    def __repr__(self):
        return "<{} id:{}>".format(
            self.__class__.__name__ , self.id
        )

    def __str__(self):
        return "K8sCluster(id={})".format(
            self.__class__.__name__. self.id
        )

    def __dir__(self):
        return self.display_columns

    def __getitem__(self, item):
        return getattr(self, self.__dir__()[item])

    def set_display_columns(self, columns):
        self.display_columns = columns

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
