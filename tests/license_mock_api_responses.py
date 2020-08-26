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

    BaseTestCase.registerHttpPostHandler(
        url="https://127.0.0.1:8080/api/v2/hpelicense",
        response=MockResponse(
            json_data={},
            status_code=201,
            headers={"location": "/api/v2/hpeclicense/1"},
        ),
    )

    BaseTestCase.registerHttpDeleteHandler(
        url="https://127.0.0.1:8080/api/v2/hpelicense/TEST_LICENSE_KEY/",
        response=MockResponse(
            json_data={},
            status_code=200,
            headers=dict(),
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/license",
        response=MockResponse(
            json_data={
                "_links": {"self": {"href": "/api/v1/license"}},
                "state": "unlicensed",
                "uuid": "3c831f6e-f76f-410d-977c-ed13b0c817d1",
            },
            status_code=200,
            headers=dict(),
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v2/hpelicense",
        response=MockResponse(
            json_data={
                "_links": {"self": {"href": "/api/v2/hpelicense"}},
                "Licenses": [
                    {
                        "Label": "The License",
                        "Feature": "HPE Machine Learning Ops",
                        "Capacity": 240,
                        "UnlimitedCapacity": False,
                        "Start": 1566864000000,
                        "StartDisplay": "2019-08-27T00:00:00Z",
                        "Expiration": 1609286399000,
                        "ExpirationDisplay": "2020-12-29T23:59:59Z",
                        "LicenseKey": "TEST_LICENSE_KEY",
                        "DeviceID": "1234 1234",
                        "Evaluation": False,
                    }
                ],
                "Summaries": [
                    {
                        "Label": "HPE Container Platform",
                        "UnlimitedCapacity": False,
                        "TotalCapacity": 240,
                        "UsedCapacity": 24,
                        "AvailableCapacity": 216,
                        "NextExpiration": 1609286399000,
                        "NextExpirationDisplay": "2020-12-29T23:59:59Z",
                        "LatestExpiration": 1609286399000,
                        "LatestExpirationDisplay": "2020-12-29T23:59:59Z",
                        "Valid": True,
                        "ValidationTime": 1594758782000,
                        "RevalidateTime": 1609286400000,
                    },
                    {
                        "Label": "HPE Machine Learning Ops",
                        "UnlimitedCapacity": False,
                        "TotalCapacity": 240,
                        "UsedCapacity": 0,
                        "AvailableCapacity": 240,
                        "NextExpiration": 1609286399000,
                        "NextExpirationDisplay": "2020-12-29T23:59:59Z",
                        "LatestExpiration": 1609286399000,
                        "LatestExpirationDisplay": "2020-12-29T23:59:59Z",
                        "Valid": True,
                        "ValidationTime": 1594758782000,
                        "RevalidateTime": 1609286400000,
                    },
                ],
                "Messages": [],
                "Valid": True,
                "Enabled": True,
                "ValidationTime": 1594758782000,
                "RevalidateTime": 1609286400000,
            },
            status_code=200,
            headers=dict(),
        ),
    )
