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

import unittest

from hpecp.base_resource import (
    AbstractResourceController,
    AbstractWaitableResourceController,
)
from hpecp.client import ContainerPlatformClient


class TestBaseResource(unittest.TestCase):
    def test_getters_and_setters(self):
        client = ContainerPlatformClient(
            username="test",
            password="test",
            api_host="test",
            api_port=8080,
            use_ssl=True,
            verify_ssl=True,
            warn_ssl=True,
        )

        class ImplClass(AbstractResourceController):
            base_resource_path = "abc"
            resource_class = "abc"
            resource_list_path = "abc"

        c = ImplClass(client)

        c._set_base_resource_path("test_base_resource_path")
        c._set_resource_class("test_resource_class")
        c._set_resource_list_path("test_resource_list_path")

        self.assertEqual(
            c._get_base_resource_path(), "test_base_resource_path"
        )
        self.assertEqual(c._get_resource_class(), "test_resource_class")
        self.assertEqual(
            c._get_resource_list_path(), "test_resource_list_path"
        )

        class ImplWaitClass(AbstractWaitableResourceController):
            status_class = "abc"
            status_fieldname = "abc"
            base_resource_path = "abc"
            resource_class = "abc"
            resource_list_path = "abc"

        c = ImplWaitClass(client)

        c._set_status_class("test_status_class")
        c._set_status_fieldname("test_status_fieldname")

        self.assertEqual(c._get_status_class(), "test_status_class")
        self.assertEqual(c._get_status_fieldname(), "test_status_fieldname")
