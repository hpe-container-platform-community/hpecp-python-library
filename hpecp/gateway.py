from __future__ import absolute_import
from .logger import Logger

from operator import attrgetter
from tabulate import tabulate
import polling


class GatewayController:

    def __init__(self, client):
        self.client = client

    def create_with_ssh_password(self, username, password):
        """Not Implemented yet"""
        raise NotImplementedError()

    def create_with_ssh_key(self, ip, proxy_node_hostname, ssh_key_data, tags=[]):
        '''Create a gateway instance using SSH key credentials to access the host

        Args:
            ip : str
                TODO
            TODO : str
                TODO ...

            Returns: gateway ID
        '''

        data = {
                "ip": ip,
                "credentials": {
                    "type": "ssh_key_access",
                    "ssh_key_data": ssh_key_data
                },
                "tags": tags,
                "proxy_nodes_hostname": proxy_node_hostname,
                "purpose": "proxy"
            },

        response = self.client._request(url='/api/v1/workers/', http_method='post', data=data, description='worker/create_with_ssh_key')
        return response.headers['location']

    def list(self):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/api/v1/workers/', http_method='get', description='worker/list')
        return [ worker for worker in response.json()["_embedded"]["workers"] if worker['purpose'] == 'proxy' ]

    def get(self, id):
        """
        See: https://<<controller_ip>>/apidocs/site-admin-api.html for the schema of the  response object
        """
        response = self.client._request(url='/api/v1/workers/', http_method='get', description='worker/get_gateways')
        workers = response.json()["_embedded"]["workers"]
        return [ worker for worker in workers if worker['purpose'] == 'proxy' and worker['_links']['self']['href'].split('/')[-1] == str(id) ][0]

    # TODO use an enum like WorkerK8sStatus
    # TODO rename state parameter to states
    def wait_for_state(self, id, state=[], timeout_secs=60):
        """
        Uses: https://github.com/justiniso/polling/blob/master/polling.py

        status: WorkerK8sStatus value, e.g. WorkerK8sStatus.configured

        raises: Exception
        """
        assert timeout_secs >= 0, "'timeout_secs' must be >= 0"

        try:
            polling.poll(
                lambda: self.get(id)['state'] in state,
                step=10,
                poll_forever=False,
                timeout=timeout_secs
            )
        except polling.TimeoutException:
            message = "Timed out waiting for status: '{}' on Gateway ID: {}".format(state, id)
            self.client.log.error(message)
            raise Exception(message)

        self.client.log.info("Gateway ID: {} was detected to have state {}".format(id, state))