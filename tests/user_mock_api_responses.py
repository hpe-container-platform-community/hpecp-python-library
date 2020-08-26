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


from .base import BaseTestCase, MockResponse


def mockApiSetup():

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/user/",
        response=MockResponse(
            json_data={
                "_embedded": {
                    "users": [
                        {
                            "_links": {"self": {"href": "/api/v1/user/16"}},
                            "label": {"name": "csnow", "description": "chris"},
                            "is_group_added_user": False,
                            "is_external": False,
                            "is_service_account": False,
                            "default_tenant": "",
                            "is_siteadmin": False,
                        },
                        {
                            "_links": {"self": {"href": "/api/v1/user/5"}},
                            "label": {
                                "name": "admin",
                                "description": "BlueData Administrator",
                            },
                            "is_group_added_user": False,
                            "is_external": False,
                            "is_service_account": False,
                            "default_tenant": "/api/v1/tenant/1",
                            "is_siteadmin": True,
                        },
                    ]
                }
            },
            status_code=200,
            headers={},
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/user/16/",
        response=MockResponse(
            json_data={
                "_links": {"self": {"href": "/api/v1/user/16"}},
                "label": {"name": "csnow", "description": "chris"},
                "is_group_added_user": False,
                "is_external": False,
                "is_service_account": False,
                "default_tenant": "",
                "is_siteadmin": False,
            },
            status_code=200,
            headers={},
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/user/123",
        response=MockResponse(
            json_data={
                "_links": {"self": {"href": "/api/v1/user/123"}},
                "purpose": "proxy",
            },
            status_code=200,
            headers={},
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/user/999",
        response=MockResponse(
            text_data="Not found.",
            json_data={},
            status_code=404,
            raise_for_status_flag=True,
            headers={},
        ),
    )

    BaseTestCase.registerHttpPostHandler(
        url="https://127.0.0.1:8080/api/v1/user",
        response=MockResponse(
            json_data={},
            status_code=200,
            headers={"location": ("/mock/api/user/1")},
        ),
    )

    BaseTestCase.registerHttpDeleteHandler(
        url="https://127.0.0.1:8080/api/v1/user/999",
        response=MockResponse(
            text_data="Not found.",
            json_data={},
            status_code=404,
            raise_for_status_flag=True,
            headers={},
        ),
    )

    BaseTestCase.registerHttpDeleteHandler(
        url="https://127.0.0.1:8080/api/v1/user/123",
        response=MockResponse(
            text_data="",
            json_data={},
            status_code=200,
            headers={},
        ),
    )
