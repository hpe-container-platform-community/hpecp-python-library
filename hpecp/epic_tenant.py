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

class EpicTenant():

    def __init__(self, json):
        self.json = json

    @property
    def status(self): return self.json['status']

    @property
    def name(self): return self.json['label']['name']

    @property
    def description(self): return self.json['label']['description']

class EpicTenantList():

    def __init__(self, json):
        self.tenants = [EpicTenant(t) for t in json]

    def __getitem__(self, item):
        return self.tenants[item]

    def __next__(self):
        if not self.tenants:
           raise StopIteration
        return self.tenants.pop()

    def __iter__(self):
        return self

class EpicTenantController:

    def __init__(self, client):
        self.client = client

    def list(self):
        response = self.client._request(url='/tenant', http_method='get', description='epic_tenant_list')
        tenants = EpicTenantList(response.json()['_embedded']['tenants'])
        return tenants

