from __future__ import absolute_import
from .logger import Logger

from operator import attrgetter
from tabulate import tabulate
import polling


class EpicWorkerController:

    def __init__(self, client):
        self.client = client

    # TODO return gateway object
    def add_gateway(self, data):
        '''
        Example:
            data = {
                "ip":"10.1.0.105",
                "credentials":{
                    "type":"ssh_key_access",
                    "ssh_key_data":"-----BEGIN RSA PRIVATE KEY-----...-----END RSA PRIVATE KEY-----\n"
                },
                "tags":[],
                "proxy_nodes_hostname":"ip-10-1-0-19.eu-west-2.compute.internal",
                "purpose":"proxy"
            },

            Returns: gateway ID
        '''
        response = self.client._request(url='/api/v1/workers/', http_method='post', data=data, description='worker/add_gateway')
        return response.headers['location'].split('/')[-1]

    def get_gateways(self):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/api/v1/workers/', http_method='get', description='worker/get_gateways')
        return [ worker for worker in response.json()["_embedded"]["workers"] if worker['purpose'] == 'proxy' ]

    def get_gateway(self, id):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/api/v1/workers/', http_method='get', description='worker/get_gateways')
        workers = response.json()["_embedded"]["workers"]
        return [ worker for worker in workers if worker['purpose'] == 'proxy' and worker['_links']['self']['href'].split('/')[-1] == str(id) ][0]

    # TODO use an enum like WorkerK8sStatus
    # TODO rename state parameter to states
    def wait_for_gateway_state(self, id, state=[], timeout_secs=60):
        """
        Uses: https://github.com/justiniso/polling/blob/master/polling.py

        status: WorkerK8sStatus value, e.g. WorkerK8sStatus.configured

        raises: Exception
        """
        assert timeout_secs >= 0, "'timeout_secs' must be >= 0"

        try:
            polling.poll(
                lambda: self.get_gateway(id)['state'] in state,
                step=10,
                poll_forever=False,
                timeout=timeout_secs
            )
        except polling.TimeoutException:
            message = "Timed out waiting for status: '{}' on Gateway ID: {}".format(state, id)
            self.client.log.error(message)
            raise Exception(message)

        self.client.log.info("Gateway ID: {} was detected to have state {}".format(id, state))