from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
import time
import requests 
import json
import urllib

class LicenseController:

    def __init__(self, client):
        self.client = client

    def platform_id(self):
        """Retrieve the Platform ID"""
        response = self.client._request(url='/api/v1/license', http_method='get', description='license/get_platform_id')
        return response.json()['uuid']

    def list(self):
        """Retrieve the list of licenses
        """
        response = self.client._request(url='/api/v2/hpelicense', http_method='get', description='license/get_license')
        return response.json()

    def upload_with_ssh_key(self, server_filename, ssh_key_file=None, ssh_key_data=None, base64enc_license=''):
        """Not implemented yet! 

        Workaround: 
         - scp your license to '/srv/bluedata/license/' on the controller
         - run client.license.register(server_filename) to register the license
        """
        raise Exception("Not implemented yet! Workaround: scp your license to '/srv/bluedata/license/'")  
        
    def upload_with_ssh_pass(self, server_filename, ssh_username, ssh_password, base64enc_license=''):
        """Not implemented yet! 

        Workaround: 
         - scp your license to '/srv/bluedata/license/' on the controller
         - run client.license.register(server_filename) to register the license
        """
        raise Exception("Not implemented yet! Workaround: scp your license to '/srv/bluedata/license/'")  


    def register(self, server_filename):
        """Register a license that has been uploaded to '/srv/bluedata/license/' on the controller.

        Arguments:

            server_filename: str
                Filepath to the license on the server, e.g. '/srv/bluedata/license/LICENSE-1.txt'

        Raises:

            APIException
        """
        data = { "hpelicense_file": server_filename }
        return self.client._request(url='/api/v2/hpelicense', http_method='post', data=data, description='license/register')

    def delete(self, license_key):
        """Delete a license by LicenseKey
        
        Arguments:

            license_key: str
                The license key, e.g. '1234 1234 ... 1234 "SOMETEXT"'

        Raises:

            APIException
        """

        try:
            lic = urllib.parse.quote(license_key)  # python 2
        except:
            lic = urllib.pathname2url(license_key) # python 3

        return self.client._request(url='/api/v2/hpelicense/{}/'.format(lic), http_method='delete', description='license/delete')

