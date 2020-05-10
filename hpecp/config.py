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

class ConfigController:

    def __init__(self, client):
        self.client = client

    def auth(self, data):
        '''
        Example::
        
            data = { 
                "external_identity_server":  {
                    "bind_pwd":"5ambaPwd@",
                    "user_attribute":"sAMAccountName",
                    "bind_type":"search_bind",
                    "bind_dn":"cn=Administrator,CN=Users,DC=samdom,DC=example,DC=com",
                    "host":"10.1.0.77",
                    "security_protocol":"ldaps",
                    "base_dn":"CN=Users,DC=samdom,DC=example,DC=com",
                    "verify_peer": False,
                    "type":"Active Directory",
                    "port":636 
                }
            }
        '''
        self.client._request(url='/api/v2/config/auth', http_method='post', data=data, description='config/auth')
