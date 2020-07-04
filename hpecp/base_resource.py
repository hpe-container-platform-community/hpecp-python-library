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
