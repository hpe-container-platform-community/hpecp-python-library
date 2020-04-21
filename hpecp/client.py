from __future__ import absolute_import

from .logger import Logger
from .epic_tenant import EpicTenant

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
                 username = None, 
                 password = None,
                 api_host = None,
                 api_port = 8080,
                 use_ssl  = True):
        
        assert isinstance(username, string_types), "'username' parameter must be of type string"
        assert isinstance(password, string_types), "'password' parameter must be of type string"
        assert isinstance(api_host, string_types), "'api_host' parameter must be of type string"
        assert isinstance(api_port, int), "'api_port' parameter must be of type int"
        assert isinstance(use_ssl, bool), "'use_ssl' parameter must be of type bool"

        self.username = username
        self.password = password
        self.api_host = api_host
        self.api_port = api_port  
        self.use_ssl  = use_ssl
        
        self.epic_tenant = EpicTenant(self)

    def create_session(self):

        if self.use_ssl:
            scheme = 'https'
        else:
            scheme = 'http'

        url = "{}://{}:{}/api/v1/login".format(scheme, self.api_host, self.api_port)
        auth = { "name": self.username, "password": self.password }

        try:
            # TODO allow verifying the ssl cert
            response = requests.post(url, json=auth, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log.error('Auth Response: ' + response.text)
            raise

        self.session_headers = response.headers
        return response

    
   

    