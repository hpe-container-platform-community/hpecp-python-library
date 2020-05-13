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
        """Retrieve the locks"""
        return self.client._request(url='/api/v1/lock', http_method='get', description='lock/get_locks').json()

    def list(self):
        """Retrieve the locks"""
        return self.get()

    def create(self, reason=None):
        """Create a new lock

        Arguments:

            reason: str
                Provide a reason for the lock

        Raises:

            APIException
        """
        data = {"reason" : reason}
        return self.client._request(url='/api/v1/lock', http_method='post', data=data, description='lock/set_lock')

    def delete(self, lock_id):
        """Delete a lock

        Arguments:

            lock_id: str
                The lock id as retrieved with `get()`  Format: '/api/v1/lock/[0-9]+'

        Raises:

            APIException
        """

        assert isinstance(lock_id, basestring),"'lock_id' must be provided and must be a string"
        assert re.match(r'\/api\/v1\/lock\/[0-9]+', lock_id), "'lock_id' must have format '/api/v1/lock/[0-9]+'"

        return self.client._request(url=lock_id, http_method='delete', description='lock/delete_lock')

    def delete_all(self, timeout_secs=300):
        """Delete all locks

        Arguments:

            timeout_secs: int
                How long to wait for internal locks (note these need to be cleared before external locks can be deleted)

        Raises:

            APIException
        """

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

