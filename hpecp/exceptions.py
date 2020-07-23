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


class ContainerPlatformClientException(Exception):
    def __init__(self, message, *args):
        self.message = message
        super(ContainerPlatformClientException, self).__init__(message, *args)


class APIException(Exception):
    def __init__(
        self, message, request_method, request_url, request_data=None, *args
    ):
        self.message = message
        self.request_method = request_method
        self.request_url = request_url
        self.request_data = request_data
        super(APIException, self).__init__(
            message, request_method, request_url, request_data, *args
        )


class APIUnknownException(APIException):
    pass


class APIItemNotFoundException(APIException):
    def __init__(
        self, message, request_method, request_url, request_data=None, *args
    ):
        self.message = message
        self.request_method = request_method
        self.request_url = request_url
        self.request_data = request_data
        super(APIItemNotFoundException, self).__init__(
            message, request_method, request_url, request_data, *args
        )


class APIForbiddenException(APIException):
    def __init__(
        self, message, request_method, request_url, request_data=None, *args
    ):
        self.message = message
        self.request_method = request_method
        self.request_url = request_url
        self.request_data = request_data
        super(APIForbiddenException, self).__init__(
            message, request_method, request_url, request_data, *args
        )


class APIItemConflictException(APIException):
    def __init__(
        self, message, request_method, request_url, request_data=None, *args
    ):
        self.message = message
        self.request_method = request_method
        self.request_url = request_url
        self.request_data = request_data
        super(APIItemConflictException, self).__init__(
            message, request_method, request_url, request_data, *args
        )
