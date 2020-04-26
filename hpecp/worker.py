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

class WorkerController:

    def __init__(self, client):
        self.client = client

    def add_k8shost(self, data):
        '''
        Example:
        
            data ={
                "ipaddr":"10.1.0.105",
                "credentials":{
                    "type":"ssh_key_access",
                    "ssh_key_data":"-----BEGIN RSA PRIVATE KEY-----...-----END RSA PRIVATE KEY-----\n"
                },
                "tags":[]
            },
        '''
        self.client._request(url='/v2/worker/k8shost/', http_method='post', data=data, description='worker/add_k8shost')
