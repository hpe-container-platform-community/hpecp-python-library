from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
import time
import requests 
import json
import urllib
import polling
import re

try:
  basestring
except NameError:
  basestring = str

class LockController:

    def __init__(self, client):
        self.client = client

    def get(self):
        return self.client._request(url='/api/v1/lock', http_method='get', description='lock/get_locks').json()

    def create(self, reason=None):
        data = {"reason" : reason}
        return self.client._request(url='/api/v1/lock', http_method='post', data=data, description='lock/set_lock')

    def delete(self, lock_id):

        assert isinstance(lock_id, basestring),"'lock_id' must be provided and must be a string"
        assert re.match(r'\/api\/v1\/lock\/[0-9]+', lock_id), "'lock_id' must have format '/api/v1/lock/[0-9]+'"

        return self.client._request(url=lock_id, http_method='delete', description='lock/delete_lock')

    def delete_all(self, timeout_secs=300):
        # we can only wait for internal locks - these need to be cleared
        # before external locks
        try:
            polling.poll(
                lambda: len(self.get()['_embedded']['internal_locks']) == 0,
                step=60,
                poll_forever=False,
                timeout=timeout_secs
                )
        except polling.TimeoutException:
            raise Exception("Timed out waiting for internal locks to free.")

        if len(self.get()['_embedded']['external_locks']) > 0:
            for lock in self.get()['_embedded']['external_locks']:
                lock_id = lock['_links']['self']['href']
                self.delete(lock_id)

        return True

