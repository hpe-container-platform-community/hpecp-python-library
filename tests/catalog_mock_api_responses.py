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


from hpecp.exceptions import APIItemNotFoundException

from .base import BaseTestCase, MockResponse


def mockApiSetup():
    BaseTestCase.registerHttpPostHandler(
        url="https://127.0.0.1:8080/api/v1/catalog/99",
        response=MockResponse(json_data={}, status_code=204, headers=dict()),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/catalog/99",
        response=MockResponse(
            json_data={
                "_links": {
                    "self": {"href": "/api/v1/catalog/99"},
                    "feed": [
                        {
                            "href": (
                                "https://s3.amazonaws.com/bluedata-catalog/"
                                "bundles/catalog/external/docker/EPIC-5.0/"
                                "feeds/feed.json"
                            ),
                            "name": (
                                "BlueData EPIC-5.0 catalog feed for docker"
                            ),
                        }
                    ],
                },
                "id": "/api/v1/catalog/99",
                "distro_id": "bluedata/spark240juphub7xssl",
                "label": {
                    "name": "Spark240",
                    "description": (
                        "Spark240 multirole with Jupyter Notebook, Jupyterhub"
                        " with SSL and gateway node"
                    ),
                },
                "version": "2.8",
                "timestamp": 0,
                "isdebug": False,
                "osclass": ["centos"],
                "logo": {
                    "checksum": "1471eb59356066ed4a06130566764ea6",
                    "url": (
                        "http://10.1.0.53/catalog/logos/"
                        "bluedata-spark240juphub7xssl-2.8"
                    ),
                },
                "documentation": {
                    "checksum": "52f53f1b2845463b9e370d17fb80bea6",
                    "mimetype": "text/markdown",
                    "file": (
                        "/opt/bluedata/catalog/documentation/"
                        "bluedata-spark240juphub7xssl-2.8"
                    ),
                },
                "state": "initialized",
                "state_info": "",
            },
            status_code=200,
            headers=dict(),
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/catalog/100",
        response=MockResponse(
            json_data={
                "_links": {
                    "self": {"href": "/api/v1/catalog/100"},
                    "feed": [
                        {
                            "href": (
                                "https://s3.amazonaws.com/bluedata-catalog/"
                                "bundles/catalog/external/docker/EPIC-5.0/"
                                "feeds/feed.json"
                            ),
                            "name": (
                                "BlueData EPIC-5.0 catalog feed for docker"
                            ),
                        }
                    ],
                },
                "id": "/api/v1/catalog/100",
                "distro_id": "bluedata/spark240juphub7xssl",
                "label": {
                    "name": "Spark240",
                    "description": (
                        "Spark240 multirole with Jupyter Notebook, Jupyterhub"
                        " with SSL and gateway node"
                    ),
                },
                "version": "2.8",
                "timestamp": 0,
                "isdebug": False,
                "osclass": ["centos"],
                "logo": {
                    "checksum": "1471eb59356066ed4a06130566764ea6",
                    "url": (
                        "http://10.1.0.53/catalog/logos/"
                        "bluedata-spark240juphub7xssl-2.8"
                    ),
                },
                "documentation": {
                    "checksum": "52f53f1b2845463b9e370d17fb80bea6",
                    "mimetype": "text/markdown",
                    "file": (
                        "/opt/bluedata/catalog/documentation/"
                        "bluedata-spark240juphub7xssl-2.8"
                    ),
                },
                "state": "initialized",
                "state_info": "",
            },
            status_code=200,
            headers=dict(),
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/catalog/101",
        response=APIItemNotFoundException(
            message="catalog not found with id: " + "/api/v1/catalog/101",
            request_method="get",
            request_url="https://127.0.0.1:8080/api/v1/catalog/101",
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/catalog/102",
        response=MockResponse(
            json_data={"garbage"},
            status_code=200,
            headers=dict(),
        ),
    )

    BaseTestCase.registerHttpGetHandler(
        url="https://127.0.0.1:8080/api/v1/catalog",
        response=MockResponse(
            json_data={
                "_links": {
                    "self": {"href": "/api/v1/catalog/"},
                    "feedlog": {"href": "/api/v1/catalog/feedlog"},
                    "feed": [
                        {
                            "href": "http://127.0.0.1:8080/api/v1/feed/local",
                            "name": "Feed generated from local bundles.",
                        },
                        {
                            "href": (
                                "https://s3.amazonaws.com/bluedata-catalog/bundles/"
                                "catalog/external/docker/EPIC-5.0/feeds/feed.json"
                            ),
                            "name": "BlueData EPIC-5.0 catalog feed for docker",
                        },
                    ],
                },
                "catalog_api_version": 6,
                "feeds_refresh_period_seconds": 86400,
                "feeds_read_counter": 5,
                "catalog_write_counter": 5,
                "_embedded": {
                    "independent_catalog_entries": [
                        {
                            "_links": {
                                "self": {"href": "/api/v1/catalog/29"},
                                "feed": [
                                    {
                                        "href": (
                                            "https://s3.amazonaws.com/bluedata-catalog/"
                                            "bundles/catalog/external/docker/EPIC-5.0/"
                                            "feeds/feed.json"
                                        ),
                                        "name": (
                                            "BlueData EPIC-5.0 catalog feed for docker"
                                        ),
                                    }
                                ],
                            },
                            "distro_id": "bluedata/spark240juphub7xssl",
                            "label": {
                                "name": "Spark240",
                                "description": (
                                    "Spark240 multirole with Jupyter Notebook, Jupyterhub"
                                    " with SSL and gateway node"
                                ),
                            },
                            "version": "2.8",
                            "timestamp": 0,
                            "isdebug": False,
                            "osclass": ["centos"],
                            "logo": {
                                "checksum": "1471eb59356066ed4a06130566764ea6",
                                "url": (
                                    "http://10.1.0.53/catalog/logos/"
                                    "bluedata-spark240juphub7xssl-2.8"
                                ),
                            },
                            "documentation": {
                                "checksum": "52f53f1b2845463b9e370d17fb80bea6",
                                "mimetype": "text/markdown",
                                "file": (
                                    "/opt/bluedata/catalog/documentation/"
                                    "bluedata-spark240juphub7xssl-2.8"
                                ),
                            },
                            "state": "initialized",
                            "state_info": "",
                        }
                    ]
                },
            },
            status_code=200,
            headers=dict(),
        ),
    )
