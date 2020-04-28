from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
import time
import requests 
import json
import urllib

class LockController:

    def __init__(self, client):
        self.client = client

    """
    Example response:

    {'_links': {'self': {'href': '/api/v1/lock'}}, 'locked': True, 'quiesced': True, '_embedded': {'internal_locks': [], 'external_locks': [{'_links': {'self': {'href': '/api/v1/lock/2'}}, 'reason': 'install', 'internal': False, 'source': 'admin'}]}}
    """
    def get_locks(self):
        response = self.client._request(url='/api/v1/lock', http_method='get', description='lock/get_locks')
        return response.json()

    def set_lock(self, reason=None):
        data = {"reason" : reason}
        response = self.client._request(url='/api/v1/lock', http_method='post', data=data, description='lock/set_lock')
        return response

    def delete_lock(self, lock_id):
        response = self.client._request(url='/api/v1/lock/{}'.format(lock_id), http_method='delete', description='lock/delete_lock')
        return response

    def delete_locks(self):
        # TODO how to handle external locks?
        if len(self.get_locks()['_embedded']['external_locks']) > 0:
            for lock in self.get_locks()['_embedded']['external_locks']:
                lock_id = lock['_links']['self']['href'].split('/')[-1]
                self.delete_lock(lock_id)
