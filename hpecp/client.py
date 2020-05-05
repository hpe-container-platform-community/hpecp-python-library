"""
This module is the main module that users of this library will interact with.
"""

from __future__ import absolute_import
from six import raise_from

from .logger import Logger
from .tenant import TenantController
from .config import ConfigController
from .epic_worker import EpicWorkerController
from .k8s_worker import K8sWorkerController
from .k8s_cluster import K8sClusterController
from .license import LicenseController
from .lock import LockController
from .exceptions import ContainerPlatformClientException, APIException, APIItemNotFoundException

import os
import requests
import json

try:
    # Python 3x
    import configparser
except:
    # Python 2.7
    import ConfigParser

import sys
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring

class ContainerPlatformClient(object):
    """The ContainerPlatformClient object is the central object that users of this library work with."""

    USER_DEFAULT_CONFIG_FILE = os.path.join(os.path.expanduser("~"), '.hpecp.conf')

    @classmethod
    def create_from_config_file(cls, config_file=USER_DEFAULT_CONFIG_FILE, profile=None):

        if profile is None:
            profile = 'default'

        if not os.path.exists(config_file):
            raise ContainerPlatformClientException(
                    "Could not found configuration file '{}'".format(config_file))

        config = configparser.ConfigParser()
        config.read(config_file)

        assert profile in config, "'{}' section not found in '{}'".format(profile, config_file)

        assert 'username' in config[profile]

        assert 'username' in config[profile] or 'username' in config['default'], "'username' not found in section '{}' or in the default section".format(profile)
        assert 'password' in config[profile] or 'password' in config['default'], "'password' not found in section '{}' or in the default section".format(profile)
        assert 'api_host' in config[profile] or 'api_host' in config['default'], "'api_host' not found in section '{}' or in the default section".format(profile)
        assert 'api_port' in config[profile] or 'api_port' in config['default'], "'api_port' not found in section '{}' or in the default section".format(profile)
        assert 'use_ssl' in config[profile] or 'use_ssl' in config['default'], "'use_ssl' not found in section '{}' or in the default section".format(profile)
        assert 'verify_ssl' in config[profile] or 'verify_ssl' in config['default'], "'verify_ssl' not found in section '{}' or in the default section".format(profile)

        def get_config_value(key, profile):
            if key in config[profile]:
                return config[profile][key]
            else:
                return config['default'][key]
            
        username = str(get_config_value('username', profile))
        password = str(get_config_value('password', profile))
        api_host = str(get_config_value('api_host', profile))
        api_port = int(get_config_value('api_port', profile))
        use_ssl = str(get_config_value('use_ssl', profile))
        verify_ssl = str(get_config_value('verify_ssl', profile))

        if use_ssl == 'False':
            use_ssl = False
        else:
            use_ssl = True

        if verify_ssl == 'False':
            verify_ssl = False
        
        return cls(username, password, api_host, api_port, use_ssl, verify_ssl)

    @classmethod
    def create_from_env(cls):
        assert 'HPECP_USERNAME' in os.environ, "'HPECP_USERNAME' environment variable not found"
        assert 'HPECP_PASSWORD' in os.environ, "'HPECP_PASSWORD' environment variable not found"
        assert 'HPECP_API_HOST' in os.environ, "'HPECP_API_HOST' environment variable not found"
        assert 'HPECP_API_PORT' in os.environ, "'HPECP_API_PORT' environment variable not found"
        assert 'HPECP_USE_SSL' in os.environ, "'HPECP_USE_SSL' environment variable not found"
        assert 'HPECP_VERIFY_SSL' in os.environ, "'HPECP_VERIFY_SSL' environment variable not found"
        return cls(username, password, api_host, api_port, use_ssl, verify_ssl)

    def __init__(self, 
                 username   = None, 
                 password   = None,
                 api_host   = None,
                 api_port   = 8080,
                 use_ssl    = True,
                 verify_ssl = True
                 ):
        """The ContainerPlatformClient object is the central object that users of this library work with.

        Parameters:
            username : str
                HPECP username
            password : str
                HPECP password
            api_host : str
                HPECP api_host 
            api_port : int
                HPECP api_port 
            use_ssl : bool:
                Connect to HPECP using SSL: True|False 
            verify_ssl : bool|str
                See https://requests.readthedocs.io/en/master/user/advanced/#ssl-cert-verification
            
        Returns:
            ContainerPlatformClient: 
                An instance of ContainerPlatformClient

        Notes:
            Instantiating the ContainerPlatformClient does not make any connection to the HPE Container Platform API. The 
            initial connection would be made by calling the method :py:meth:`create_session`.

        """
        self._log = Logger().get_logger(self.__class__.__name__)

        # TODO add other fields, except password
        self._log.debug("__init__ called with username['{}']".format(username))
        
        assert isinstance(username, string_types), "'username' parameter must be of type string"
        assert isinstance(password, string_types), "'password' parameter must be of type string"
        assert isinstance(api_host, string_types), "'api_host' parameter must be of type string"
        assert isinstance(api_port, int), "'api_port' parameter must be of type int"
        assert isinstance(use_ssl, bool), "'use_ssl' parameter must be of type bool"
        # TODO - assert verify_ssl

        self.username = username
        self.password = password
        self.api_host = api_host
        self.api_port = api_port  
        self.use_ssl  = use_ssl
        self.verify_ssl = verify_ssl
        
        if self.use_ssl:
            scheme = 'https'
        else:
            scheme = 'http'

        self.base_url = "{}://{}:{}".format(scheme, self.api_host, self.api_port)

        # register endpoint modules - see @property definitions at end of file for each module
        self._tenant = TenantController(self)
        self._config = ConfigController(self)
        self.epic_worker = EpicWorkerController(self)
        self.k8s_worker = K8sWorkerController(self)
        self._k8s_cluster = K8sClusterController(self)
        self.license = LicenseController(self)
        self.lock = LockController(self)

    def create_session(self):
        """Create a session with the HPE CP controller defined in the object :py:class:`ContainerPlatformClient`.

        Returns:
            ContainerPlatformClient: 
                An instance of ContainerPlatformClient is returned.

        Raises:
            APIException
                for connection error to the HPE CP controller
            requests.exceptions.RequestException
                for exceptions that are not a connection error
        """

        url = self.base_url + "/api/v1/login"
        auth = { "name": self.username, "password": self.password }

        response = None
        try:
            response = requests.post(url, json=auth, verify=self.verify_ssl)
            response.raise_for_status()

        except requests.exceptions.ConnectionError as e:
            raise_from(APIException(
                        message='Could not connect to controller', 
                        request_method='post', 
                        request_url=url
                        ), None)

        except requests.exceptions.RequestException as e:
            if response is not None:
                self.log.error('Auth Response: ' + response.text)
            else:
                self.log.error(e)
            raise

        self.session_headers = response.headers
        self.session_id = response.headers['location']

    def _request_headers(self):

        headers = {
            'accept': 'application/json',
            'X-BDS-SESSION': self.session_id,
            'cache-control': 'no-cache', 
            'content-type': 'application/json'
            }
        return headers

    def _request(self, url, http_method='get', data={}, description='', create_auth_headers=True, additional_headers={}):
        if create_auth_headers:
            headers = self._request_headers()
        else:
            headers = {}
            
        all_headers = {}
        all_headers.update(headers)
        all_headers.update(additional_headers)

        url = url = self.base_url + url

        try:
            if http_method == 'get':
                self.log.debug('{} : {} {}'.format(description, http_method, url))
                response = requests.get(url, headers=all_headers, verify=self.verify_ssl)
            elif http_method == 'put':
                self.log.debug('{} : {} {} {}'.format(description, http_method, url, data))
                response = requests.put(url, headers=all_headers, data=json.dumps(data), verify=self.verify_ssl)
            elif http_method == 'post':
                self.log.debug('{} : {} {} {}'.format(description, http_method, url, data))
                response = requests.post(url, headers=all_headers, data=json.dumps(data), verify=self.verify_ssl)
            elif http_method == 'delete':
                self.log.debug('{} : {} {}'.format(description, http_method, url))
                response = requests.delete(url, headers=all_headers, verify=self.verify_ssl)

            response.raise_for_status()
        except requests.exceptions.RequestException:
            try:
                response_info = response.json()
            except:
                response_info = response.text
            else:
                response_info = ''

            if response.status_code == 404:
                # This is expected for some method calls so do not log as an error
                self.log.debug('{} : {} {} Request: {}'.format(description, http_method, url, json.dumps(data)))
                raise APIItemNotFoundException(message=response_info, request_method=http_method, request_url=url, request_data=json.dumps(data))
            else:
                self.log.exception('{} : {} {} Request: {}'.format(description, http_method, url, json.dumps(data)))
                raise APIException(message=response_info, request_method=http_method, request_url=url, request_data=json.dumps(data))

        try:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, json.dumps(response.json())))
        except ValueError:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, response.text))

        return response

    
    @property
    def tenant(self):
        """
        This attribute is a reference to an object of type `.tenant.TenantController`.

        See the class :py:class:`.tenant.TenantController` for the methods available.

        Example::

            client = ContainerPlatformClient(...)
            client.create_session()
            client.tenant.list()
        
        This example calls the method :py:meth:`list() <.tenant.TenantController.list>` in :py:class:`.tenant.TenantController`.
        """

        return self._tenant

    @property
    def config(self):
        """
        This attribute is a reference to an object of type `.config.ConfigController`.

        See the class :py:class:`.config.ConfigController` for the methods available.

        Example::

            client = ContainerPlatformClient(...)
            client.create_session()
            client.config.auth(
                {
                    "external_identity_server":  {
                        "bind_pwd":"5ambaPwd@",
                        "user_attribute":"sAMAccountName",
                        "bind_type":"search_bind",
                        "bind_dn":"cn=Administrator,CN=Users,DC=samdom,DC=example,DC=com",
                        "host":"10.1.0.77",
                        "security_protocol":"ldaps",
                        "base_dn":"CN=Users,DC=samdom,DC=example,DC=com",
                        "verify_peer": False,
                        "type":"Active Directory",
                        "port":636 
                    }
                }
            )
        
        This example calls the method :py:meth:`auth() <.config.ConfigController.auth>` in :py:class:`.config.ConfigController`.
        """

        return self._config

    @property
    def k8s_cluster(self):
        """
        This attribute is a reference to an object of type `.k8s_cluster.K8sClusterController`.

        See the class :py:class:`.k8s_cluster.K8sClusterController` for the methods available.

        Example::

            client = ContainerPlatformClient(...)
            client.create_session()
            client.k8s_cluster.list()
        
        This example calls the method :py:meth:`list() <.k8s_cluster.K8sClusterController.list>` in :py:class:`.k8s_cluster.K8sClusterController`.
        """

        return self._k8s_cluster

    @property
    def log(self):
        """
        This attribute is a reference to :py:class:`.logger.Logger`.  The log function can be called from controller objects
        via the `client` parameter passed in during instantiation of the controller.

        Example::

            class K8sClusterController:
                ...

                def __init__(self, client):
                    self.client = client

                def some_method(self):
                    ...
                    self.client.log.error("Some Error")
        """

        return self._log
   

    