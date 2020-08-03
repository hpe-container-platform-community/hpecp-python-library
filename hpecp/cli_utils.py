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

"""CLI Utilities."""

from collections import OrderedDict
from io import StringIO

import six
from six import string_types

# This class has been adapted from knack.
# See https://github.com/microsoft/knack/blob/master/LICENSE


class TextOutput(object):
    """Text output class."""

    @staticmethod
    def _dump_obj(data, stream):
        if isinstance(data, list):
            stream.write(str(len(data)))
        elif isinstance(data, dict):
            # We need to print something to avoid mismatching
            # number of columns if the value is None for some instances
            # and a dictionary value in other...
            stream.write("")
        else:
            to_write = data if isinstance(data, string_types) else str(data)
            stream.write(to_write)

    @staticmethod
    def _dump_row(data, stream):
        separator = ""
        if isinstance(data, (dict, list)):
            if isinstance(data, OrderedDict):
                values = data.values()
            elif isinstance(data, dict):
                values = [value for _, value in sorted(data.items())]
            else:
                values = data

            for value in values:
                stream.write(separator)
                TextOutput._dump_obj(value, stream)
                separator = "\t"
        elif isinstance(data, list):
            for value in data:
                stream.write(separator)
                TextOutput._dump_obj(value, stream)
                separator = "\t"
        elif isinstance(data, bool):
            TextOutput._dump_obj(str(data).lower(), stream)
        else:
            TextOutput._dump_obj(data, stream)
        stream.write("\n")

    @staticmethod
    def dump(data):
        """Dump the python object as text."""  # noqa: D202

        class MyStringIO(StringIO):
            def write(self, b):
                if six.PY2:
                    val = unicode(b)  # noqa: F821
                else:
                    val = b
                super(MyStringIO, self).write(val)

        io = MyStringIO()
        for item in data:
            TextOutput._dump_row(item, io)

        result = io.getvalue()
        io.close()
        return str(result)
