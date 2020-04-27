from __future__ import absolute_import

from .logger import Logger
from .epic_tenant import EpicTenantController
from .config import ConfigController
from .worker import WorkerController
from .license import LicenseController

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
                 username   = None, 
                 password   = None,
                 api_host   = None,
                 api_port   = 8080,
                 use_ssl    = True,
                 verify_ssl = True):
        """ContainerPlatformClient object.

        Keyword arguments:
        username   -- HPECP username
        password   -- HPECP password
        api_host   -- HPECP api_host
        api_port   -- HPECP api_port
        use_ssl    -- Connect to HPECP using SSL: True|False
        verify_ssl -- Verify the HPECP SSL Certificate? True|False|path to a CA_BUNDLE file or directory with certificates of trusted CAs
        """

        self.log = Logger().get_logger(self.__class__.__name__)
        
        assert isinstance(username, string_types), "'username' parameter must be of type string"
        assert isinstance(password, string_types), "'password' parameter must be of type string"
        assert isinstance(api_host, string_types), "'api_host' parameter must be of type string"
        assert isinstance(api_port, int), "'api_port' parameter must be of type int"
        assert isinstance(use_ssl, bool), "'use_ssl' parameter must be of type bool"
        # TODO - assert verify_ssl

        self.username = username
        self.password = password
        self.api_host = api_host
        self.api_port = api_port  
        self.use_ssl  = use_ssl
        self.verify_ssl = verify_ssl
        
        if self.use_ssl:
            scheme = 'https'
        else:
            scheme = 'http'

        self.base_url = "{}://{}:{}/api".format(scheme, self.api_host, self.api_port)

        # register endpoint modules
        self.epic_tenant = EpicTenantController(self)
        self.config = ConfigController(self)
        self.worker = WorkerController(self)
        self.license = LicenseController(self)

    def create_session(self):

        url = self.base_url + "/v1/login"
        auth = { "name": self.username, "password": self.password }

        try:
            response = requests.post(url, json=auth, verify=self.verify_ssl)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log.error('Auth Response: ' + response.text)
            raise

        self.session_headers = response.headers
        self.session_id = response.headers['location']

    def _request_headers(self):

        headers = {
            'accept': 'application/json',
            'X-BDS-SESSION': self.session_id,
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

        url = url = self.base_url + url
        
        try:
            if http_method == 'get':
                response = requests.get(url, headers=all_headers, verify=self.verify_ssl)
            elif http_method == 'put':
                response = requests.put(url, headers=all_headers, data=json.dumps(data), verify=self.verify_ssl)
            elif http_method == 'post':
                response = requests.post(url, headers=all_headers, data=json.dumps(data), verify=self.verify_ssl)
            elif http_method == 'delete':
                response = requests.delete(url, headers=all_headers, verify=self.verify_ssl)

            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log.debug('{} : {} {}'.format(description, http_method, url))

            try:
                response_info = response.json()
            except:
                response_info = response.text

            raise ContainerPlatformClientException(message=response_info)

        try:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, json.dumps(response.json())))
        except ValueError:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, response.text))

        return response

    
   

    