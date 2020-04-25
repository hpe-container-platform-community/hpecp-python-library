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


        #"{u'_embedded': {u'tenants': 
        # 
        # [{u'status': u'ready', u'features': 
        #       {u'ml_project': False, u'kubernetes_access': False}, 
        #   u'persistent_supported': True, u'member_key_available': u'all_admins', u'quota': 
        #       {}, u'cluster_isolation_supported': True, 
        #   u'inusequota': 
        #       {u'disk': 0, u'cores': 0, u'memory': 0, u'persistent': 0, u'gpus': 0}, 
        #   u'external_user_groups': [], u'gpu_usage_supported': True, 
        #   u'_links': 
        #       {u'self': {u'href': u'/api/v1/tenant/1'}}, 
        #   u'filesystem_mount_supported': True, u'tenant_enforcements': [], 
        #   u'label': 
        #       {u'name': u'Site Admin', u'description': u'Site Admin Tenant for BlueData clusters'}, 
        #   u'constraints_supported': False, 
        #   u'tenant_storage_quota_supported': False}, 
        #  {u'status': u'ready', u'tenant_type': u'docker', u'features': {u'ml_project': False, u'kubernetes_access': False}, u'persistent_supported': True, u'member_key_available': u'all_admins', u'quota': {}, u'cluster_isolation_supported': True, u'inusequota': {u'disk': 0, u'cores': 0, u'memory': 0, u'persistent': 0, u'gpus': 0}, u'external_user_groups': [], u'gpu_usage_supported': True, u'_links': {u'self': {u'href': u'/api/v1/tenant/2'}}, u'filesystem_mount_supported': True, u'tenant_enforcements': [], u'label': {u'name': u'Demo Tenant', u'description': u'Demo Tenant for BlueData Clusters'}, u'constraints_supported': True, u'tenant_storage_quota_supported': True, u'qos_multiplier': 1}]}, u'_links': {u'self': {u'href': u'/api/v1/tenant'}}}"

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

