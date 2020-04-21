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

    # TODO parse response and populate EpicTenantList object
    def list(self):
        # curl -X GET -H "X-BDS-SESSION:${SESSION_ID}" http://${CONTROLLER_IP}:8080/api/v1/tenant
        response = self.client._request(url='/tenant', http_method='get', description='epic_tenant_list')
        return response.json()