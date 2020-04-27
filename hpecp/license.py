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

class LicenseController:

    def __init__(self, client):
        self.client = client

    # FIXME - This doesn't return the license key (required for delete) or the complete license details/
    #         It only seems useful for the platform id (uuid field). 
    def get_license(self):
        response = self.client._request(url='/v1/license', http_method='get', description='license/get_license')
        return response.json()

    def register(self, server_filename):
        data = { "hpelicense_file": server_filename }
        response = self.client._request(url='/v2/hpelicense', http_method='post', data=data, description='license/register')
        return response

# TODO
# DELETE /api/v2/hpelicense/ABCD..License_Key..ABCD/