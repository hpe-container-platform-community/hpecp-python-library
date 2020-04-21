from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
import time
import requests
import json

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

class EpicTenant:

    def __init__(self, client):
        self.client = client


    # curl -X GET -H "X-BDS-SESSION:${SESSION_ID}" http://${CONTROLLER_IP}:8080/api/v1/tenant
    def list(self):
        #url = self.region.rc_endpoint() + '/v1/resource_instances'
        #response = self.client._request(url=url, http_method='post', description='create_resource_instances', data=data)
        #return response.json()
        raise BaseException('Not implemented yet!')