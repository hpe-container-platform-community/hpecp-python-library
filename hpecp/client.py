from __future__ import absolute_import

from .logger import Logger


import requests
import json
from datetime import datetime, timedelta

import sys
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring

class ContainerPlatformClientException(Exception):
    def __init__(self, message, *args):
        self.message = message
        super( ContainerPlatformClientException, self).__init__(message, *args) 

class ContainerPlatformClient(object):

    def __init__(self, 
                 api_key = None, 
                 api_key_filename = None,
                 region = 'us-south',
                 provision_poll_timeout_mins = 30):
        pass
    
    def _request_headers(self):

        auth_token = self.get_auth_token()
        access_token = auth_token['access_token']
        token_type = auth_token['token_type']

        headers = {
            'accept': 'application/json',
            'authorization': '{} {}'.format(token_type, access_token),
            'cache-control': 'no-cache', 
            'content-type': 'application/json'
            }
        return headers

    def _request(self, url, http_method='get', data=None, description='', create_auth_headers=True, additional_headers={}):
        if create_auth_headers:
            headers = self._request_headers()
        else:
            headers = {}
            
        all_headers = {}
        all_headers.update(headers)
        all_headers.update(additional_headers)
        
        try:
            if http_method == 'get':
                response = requests.get(url, headers=all_headers)
            elif http_method == 'post':
                response = requests.post(url, headers=all_headers, data=json.dumps(data))
            elif http_method == 'delete':
                response = requests.delete(url, headers=all_headers)

            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, response.text))
            raise ContainerPlatformClientException(message=response.text)

        try:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, json.dumps(response.json())))
        except ValueError:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, response.text))

        return response

    