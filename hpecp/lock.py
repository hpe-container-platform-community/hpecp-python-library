# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from __future__ import absolute_import

import re

import polling
from requests.structures import CaseInsensitiveDict

try:
    basestring
except NameError:
    basestring = str


class LockController:
    def __init__(self, client):
        self.client = client

    def get(self):
        """Retrieve the locks"""
        return self.client._request(
            url="/api/v1/lock", http_method="get", description="lock/get_locks"
        ).json()

    def list(self):
        """Retrieve the locks"""
        return self.get()

    def create(self, reason=None):
        """Create a new lock.

        Arguments
        ---------
        reason: str
            Provide a reason for the lock.

        Raises
        ------
        APIException
        """
        data = {"reason": reason}
        response = self.client._request(
            url="/api/v1/lock",
            http_method="post",
            data=data,
            description="lock/set_lock",
        )
        return CaseInsensitiveDict(response.headers)["Location"]

    def delete(self, lock_id):
        """Delete a lock.

        Parameters
        ----------
        lock_id: str
            The lock id as retrieved with `get()`  Format:
            '/api/v1/lock/[0-9]+'

        Raises
        ------
        APIException
        """

        assert isinstance(
            lock_id, basestring
        ), "'lock_id' must be provided and must be a string"
        assert re.match(
            r"\/api\/v1\/lock\/[0-9]+", lock_id
        ), "'lock_id' must have format '/api/v1/lock/[0-9]+'"

        return self.client._request(
            url=lock_id, http_method="delete", description="lock/delete_lock"
        )

    def delete_all(self, timeout_secs=300):
        """Delete all locks.

        Parameters
        ----------
        timeout_secs: int
            How long to wait for internal locks (note these need to be
            cleared before external locks can be deleted)

        Raises
        ------
        APIException
        """

        try:
            polling.poll(
                lambda: len(self.get()["_embedded"]["internal_locks"]) == 0,
                step=10,
                poll_forever=False,
                timeout=timeout_secs,
            )
        except polling.TimeoutException:
            return False
        except Exception as e:
            self.client.log.error(e)
            return False

        if len(self.get()["_embedded"]["external_locks"]) > 0:
            for lock in self.get()["_embedded"]["external_locks"]:
                lock_id = lock["_links"]["self"]["href"]
                self.delete(lock_id)

        return True
