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

"""HPE Container Platform Client."""

from __future__ import absolute_import

import ast
import codecs
import json
import os
import re
from configparser import SafeConfigParser

import pkg_resources
import requests
from requests.structures import CaseInsensitiveDict
from six import raise_from
from urllib3.exceptions import (
    ConnectTimeoutError,
    MaxRetryError,
    NewConnectionError,
)

from hpecp.exceptions import APIForbiddenException

from .catalog import CatalogController
from .config import ConfigController
from .datatap import DatatapController
from .exceptions import (
    APIException,
    APIItemConflictException,
    APIItemNotFoundException,
    APIUnknownException,
    ContainerPlatformClientException,
)
from .gateway import GatewayController
from .k8s_cluster import K8sClusterController
from .k8s_worker import K8sWorkerController
from .license import LicenseController
from .lock import LockController
from .logger import Logger
from .role import RoleController
from .tenant import TenantController
from .user import UserController

try:
    basestring
except NameError:
    basestring = str


class ContainerPlatformClient(object):
    """Client object for HPE Container Platform.

    This is the central object that users of this library work with.

    Parameters
    ----------
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
        See "https://requests.readthedocs.io/en/master/user/advanced/
        #ssl-cert-verification"
    warn_ssl : bool
        Disable ssl warnings
    tenant : str (optional)
        The tenant ID, e.g. /api/v1/tenant/2

    Returns
    -------
    ContainerPlatformClient:
        An instance of ContainerPlatformClient

    Notes
    -----
    Instantiating the ContainerPlatformClient does not make any connection
    to the HPE Container Platform API. The initial connection would be made
    by calling the method :py:meth:`create_session`.

    See Also
    --------
    :py:meth:`create_from_config_file` for an alternative way to create a
    ContainerPlatformClient instance
    :py:meth:`create_from_env` for an alternative way to create a
    ContainerPlatformClient instance
    """

    @classmethod
    def version(cls):
        """Retrieve the hpecp version information."""
        return pkg_resources.require("hpecp")[0].version

    @classmethod
    def create_from_config_file(
        cls, config_file="~/.hpecp.conf", profile=None
    ):
        """Create a ContainerPlatformClient object from a configuration file.

        Parameters
        ----------
        config_file : str
            The configuration filename and path
        profile : str
            If the configuration file has multiple profile sections, you
            can select the profile to use.

        Returns
        -------
        ContainerPlatformClient:
            An instance of ContainerPlatformClient is returned.

        Example
        -------
        Below is an example configuration file.

        [default]
        api_host = 127.0.0.1
        api_port = 8080
        use_ssl = True
        verify_ssl = False
        warn_ssl = False

        [demoserver]
        username = admin
        password = admin123
        tenant = /api/v1/tenant/2
        """
        _log = Logger.get_logger()

        if profile is None:
            profile = "default"

        if config_file.startswith("~"):
            file_path = config_file[1:]
            file_path = file_path.lstrip("/")
            config_file = os.path.join(os.path.expanduser("~"), file_path)

        if not os.path.exists(config_file):
            raise ContainerPlatformClientException(
                "Could not find configuration file '{}'".format(config_file)
            )

        config = SafeConfigParser()
        config.readfp(codecs.open(config_file, "r", "utf8"))

        assert (
            profile in config.sections()
        ), "'{}' section not found in '{}'".format(profile, config_file)
        assert (
            "username" in config[profile] or "username" in config["default"]
        ), (
            "'username' not found in section '{}' or in "
            "the default section".format(profile)
        )
        assert (
            "password" in config[profile] or "password" in config["default"]
        ), (
            "'password' not found in section '{}' "
            "or in the default section".format(profile)
        )
        assert (
            "api_host" in config[profile] or "api_host" in config["default"]
        ), (
            "'api_host' not found in section '{}' or in "
            "the default section".format(profile)
        )
        assert (
            "api_port" in config[profile] or "api_port" in config["default"]
        ), (
            "'api_port' not found in section '{}' or in "
            "the default section".format(profile)
        )
        assert (
            "use_ssl" in config[profile] or "use_ssl" in config["default"]
        ), (
            "'use_ssl' not found in section '{}' or in"
            "the default section".format(profile)
        )
        assert (
            "verify_ssl" in config[profile]
            or "verify_ssl" in config["default"]
        ), (
            "'verify_ssl' not found in section '{}' or in"
            "the default section".format(profile)
        )
        assert (
            "warn_ssl" in config[profile] or "warn_ssl" in config["default"]
        ), (
            "'warn_ssl' not found in section '{}' or in"
            "the default section".format(profile)
        )

        # tenant parameter is optional

        def get_config_value(key, profile):
            if key in config[profile]:
                _log.debug("Found '{}' in profile '{}'".format(key, profile))
                return config[profile][key]
            else:
                try:
                    val = config["default"][key]
                    _log.debug(
                        "Found '{}' in profile '{}'".format(key, "default")
                    )
                    return val
                except Exception:
                    _log.debug(
                        "Could not find '{}' in profile '{}'".format(
                            key, profile
                        )
                    )
                    return None

        username = str(get_config_value("username", profile))
        password = str(get_config_value("password", profile))
        api_host = str(get_config_value("api_host", profile))
        api_port = int(get_config_value("api_port", profile))
        use_ssl = str(get_config_value("use_ssl", profile))
        verify_ssl = str(get_config_value("verify_ssl", profile))
        warn_ssl = str(get_config_value("warn_ssl", profile))

        # optional parameter
        tenant = get_config_value("tenant", profile)
        if tenant:
            assert isinstance(tenant, str) and re.match(
                r"\/api\/v1\/tenant\/[0-9]+", tenant
            ), (
                "'tenant' must have format '/api/v1/tenant/[0-9]+' in '{}'"
            ).format(
                config_file
            )

        if use_ssl == "False":
            use_ssl = False
        else:
            use_ssl = True

        # verify_ssl could be a path
        if verify_ssl == "False":
            verify_ssl = False

        if warn_ssl == "False":
            warn_ssl = False
        else:
            warn_ssl = True

        return cls(
            username,
            password,
            api_host,
            api_port,
            use_ssl,
            verify_ssl,
            warn_ssl,
            tenant,
        )

    @classmethod
    def create_from_env(cls):
        """Create an instance of ContainerPlatformClient from environment variables.

        Variables
        ---------
        HPECP_USERNAME
        HPECP_PASSWORD
        HPECP_API_HOST
        HPECP_API_PORT
        HPECP_USE_SSL
        HPECP_VERIFY_SSL
        HPECP_WARN_SSL
        HPECP_TENANT

        See Also
        --------
        See ContainerPlatformClient
        :py:class:`constructor <ContainerPlatformClient>` for the paramaeter
        definitions.
        """
        try:
            HPECP_USERNAME = os.environ["HPECP_USERNAME"]
            HPECP_PASSWORD = os.environ["HPECP_PASSWORD"]
            HPECP_API_HOST = os.environ["HPECP_API_HOST"]
            HPECP_API_PORT = int(os.environ["HPECP_API_PORT"])

            HPECP_USE_SSL = ast.literal_eval(os.environ["HPECP_USE_SSL"])
            HPECP_VERIFY_SSL = ast.literal_eval(os.environ["HPECP_VERIFY_SSL"])
            HPECP_WARN_SSL = ast.literal_eval(os.environ["HPECP_WARN_SSL"])

            # Optional parameter
            HPECP_TENANT = os.getenv("HPECP_TENANT", default=None)

            if HPECP_TENANT:
                assert isinstance(HPECP_TENANT, str) and re.match(
                    r"\/api\/v1\/tenant\/[0-9]+", HPECP_TENANT
                ), (
                    "'tenant' must have format '/api/v1/tenant/[0-9]+' in "
                    "env var 'HPECP_TENANT'"
                )

        except KeyError as ke:
            raise ContainerPlatformClientException(
                "Required env var '{}' not found.".format(ke.args[0])
            )
        except ValueError as ve:
            # TODO replace with asssertions
            raise ContainerPlatformClientException(ve.args[0])

        return cls(
            username=HPECP_USERNAME,
            password=HPECP_PASSWORD,
            api_host=HPECP_API_HOST,
            api_port=HPECP_API_PORT,
            use_ssl=HPECP_USE_SSL,
            verify_ssl=HPECP_VERIFY_SSL,
            warn_ssl=HPECP_WARN_SSL,
            tenant=HPECP_TENANT,
        )

    def __init__(
        self,
        username=None,
        password=None,
        api_host=None,
        api_port=8080,
        use_ssl=True,
        verify_ssl=True,
        warn_ssl=False,
        tenant=None,
    ):
        """Create a Client object for interacting with HPE Container Platform.

        Parameters
        ----------
        username : str
            HPECP Username
        password : str
            HPECP Password
        api_host : str,
            HPECP API Host
        api_port : int, optional
            HPECP API Port, by default 8080
        use_ssl : bool, optional
            Connect to HPECP using SSL:, by default True
        verify_ssl : bool, optional
            See "https://requests.readthedocs.io/en/master/user/advanced/
            #ssl-cert-verification", by default True
        warn_ssl : bool, optional
            Disable ssl warnings, by default False
        tenant : str, optional
            The tenant ID, e.g. /api/v1/tenant/2
        """
        self._log = Logger.get_logger()

        if verify_ssl == "True":
            verify_ssl = True

        if verify_ssl == "False":
            verify_ssl = False

        self._log.debug(
            "ContainerPlatformClient() created with '{}'".format(
                {
                    "username": username,
                    "password": "********",
                    "api_host": api_host,
                    "api_port": api_port,
                    "use_ssl": use_ssl,
                    "verify_ssl": verify_ssl,
                    "warn_ssl": warn_ssl,
                    "tenant": tenant,
                }
            )
        )

        assert isinstance(
            username, basestring
        ), "'username' parameter must be of type string"
        assert isinstance(
            password, basestring
        ), "'password' parameter must be of type string"
        assert isinstance(
            api_host, basestring
        ), "'api_host' parameter must be of type string"
        assert isinstance(
            api_port, int
        ), "'api_port' parameter must be of type int"
        assert isinstance(
            use_ssl, bool
        ), "'use_ssl' parameter must be of type bool"
        assert isinstance(verify_ssl, bool) or (
            isinstance(verify_ssl, basestring)
            and os.access(verify_ssl, os.R_OK)
        ), (
            "'verify_ssl' parameter must be of type bool or point to a "
            "certificate file"
        )
        assert isinstance(
            warn_ssl, bool
        ), "'warn_ssl' parameter must be of type bool"

        self.username = username
        self.password = password
        self.api_host = api_host
        self.api_port = api_port
        self.use_ssl = use_ssl
        self.verify_ssl = verify_ssl
        self.warn_ssl = warn_ssl
        self.tenant_config = tenant

        if self.use_ssl:
            scheme = "https"
        else:
            scheme = "http"

        self.base_url = "{}://{}:{}".format(
            scheme, self.api_host, self.api_port
        )

        # Register endpoint modules - see @property definitions at end of file
        # for each module
        self._tenant = TenantController(self)
        self._config = ConfigController(self)
        self._gateway = GatewayController(self)
        self._k8s_worker = K8sWorkerController(self)
        self._k8s_cluster = K8sClusterController(self)
        self._license = LicenseController(self)
        self._lock = LockController(self)
        self._user = UserController(self)
        self._catalog = CatalogController(self)
        self._role = RoleController(self)
        self._datatap = DatatapController(self)

    def create_session(self):
        """Create a session with the HPE CP controller.

        Returns
        -------
        ContainerPlatformClient
            An instance of ContainerPlatformClient is returned.

        Raises
        ------
        APIException
            for connection error to the HPE CP controller
            requests.exceptions.RequestException
            for exceptions that are not a connection error
        """
        url = self.base_url + "/api/v1/login"
        auth = {"name": self.username, "password": self.password}

        if self.tenant_config:
            auth["tenant"] = self.tenant_config

        if self.warn_ssl is False:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # if self.log.level == 10:  # "DEBUG"
        #     if six.PY3:
        #         import http.client

        #         http.client.HTTPConnection.debuglevel = 1

        #     requests_log = logging.getLogger("requests.packages.urllib3")
        #     requests_log.setLevel(logging.DEBUG)
        #     requests_log.propagate = True

        response = None
        try:
            self.log.debug("REQ: {} : {} {}".format("Login", "post", url))
            response = requests.post(
                url, json=auth, verify=self.verify_ssl, timeout=10
            )  # 10 seconds
            response.raise_for_status()

        except (
            requests.exceptions.ConnectionError,
            NewConnectionError,
            MaxRetryError,
            ConnectTimeoutError,
        ) as e:
            self.log.debug(
                "RES: {} : {} {} {}".format("Login", "post", url, str(e))
            )
            if self.log.level == 10:  # "DEBUG"
                # The error is already output to the log, so this message
                # can be brief.
                msg = "Could not connect to the controller."
            else:
                msg = "Could not connect to the controller.\n" + str(e)
            raise_from(
                APIException(
                    message=msg, request_method="post", request_url=url,
                ),
                None,
            )

        except requests.exceptions.RequestException as e:
            if response is not None:
                self.log.error("Auth Response: " + response.text)
            else:
                self.log.error(e)
            raise

        # except Exception as e:
        #     if response is not None:
        #         self.log.error("Auth Response: " + response.text)
        #     else:
        #         self.log.error(e)
        #     raise_from(
        #         APIUnknownException(
        #             message=str(e), request_method="post", request_url=url,
        #         ),
        #         None,
        #     )

        self.session_headers = CaseInsensitiveDict(response.headers)
        self.session_id = CaseInsensitiveDict(response.headers)["location"]

        return self

    def _request_headers(self):

        headers = {
            "accept": "application/json",
            "X-BDS-SESSION": self.session_id,
            "cache-control": "no-cache",
            "content-type": "application/json",
        }
        return headers

    def _request(
        self,
        url,
        http_method="get",
        data={},
        description="",
        create_auth_headers=True,
        additional_headers={},
    ):
        """Make HTTP requests to the API host.

        Parameters
        ----------
        url : str
            This will be suffixed to the API host's address.
            Example '/api/v1/catalog/[0-9]+'
        http_method : str, optional
            HTTP method to be executed, by default "get"
        data : dict, optional
            Request payload (applicable for "post", "put"), by default {}
        description : str, optional
            Brief description about the request. , by default ""
        create_auth_headers : bool, optional
            By default True
        additional_headers : dict, optional
            Any additional headers to be passed while making the request,
            by default {}

        Returns
        -------
        Response
            The http response object

        Raises
        ------
        APIItemNotFoundException
        APIItemConflictException
        APIException
        """
        if create_auth_headers:
            headers = self._request_headers()
        else:
            headers = {}

        all_headers = {}
        all_headers.update(headers)
        all_headers.update(additional_headers)

        url = url = self.base_url + url

        if self.warn_ssl is False:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            if http_method == "get":
                self.log.debug(
                    "REQ: {} : {} {}".format(description, http_method, url)
                )
                response = requests.get(
                    url, headers=all_headers, verify=self.verify_ssl
                )
            elif http_method == "put":
                self.log.debug(
                    "REQ: {} : {} {} {}".format(
                        description, http_method, url, json.dumps(data)
                    )
                )
                response = requests.put(
                    url,
                    headers=all_headers,
                    data=json.dumps(data),
                    verify=self.verify_ssl,
                )
            elif http_method == "post":
                self.log.debug(
                    "REQ: {} : {} {} {}".format(
                        description, http_method, url, json.dumps(data)
                    )
                )
                response = requests.post(
                    url,
                    headers=all_headers,
                    data=json.dumps(data),
                    verify=self.verify_ssl,
                )
            elif http_method == "delete":
                self.log.debug(
                    "REQ: {} : {} {}".format(description, http_method, url)
                )
                response = requests.delete(
                    url, headers=all_headers, verify=self.verify_ssl
                )

            response.raise_for_status()
        except requests.exceptions.RequestException as re:
            try:
                response_info = response.json()
            except Exception:
                response_info = response.text
            else:
                response_info = ""

            def log_response():
                self.log.debug(
                    "RES: {} : {} {} : {} {}".format(
                        description,
                        http_method,
                        url,
                        response.status_code,
                        response_info,
                    )
                )

            if response.status_code == 403:
                # This is expected for some method calls so do not log as an
                # error
                log_response()
                raise APIForbiddenException(
                    message=response_info,
                    request_method=http_method,
                    request_url=url,
                    request_data=json.dumps(data),
                )
            if response.status_code == 404:
                # This is expected for some method calls so do not log as an
                # error
                log_response()
                raise APIItemNotFoundException(
                    message=response_info,
                    request_method=http_method,
                    request_url=url,
                    request_data=json.dumps(data),
                )
            if response.status_code == 409:
                # This is expected for some method calls so do not log as an
                # error
                log_response()
                raise APIItemConflictException(
                    message=response_info,
                    request_method=http_method,
                    request_url=url,
                    request_data=json.dumps(data),
                )
            else:
                log_response()
                raise APIUnknownException(
                    message=str(re),  # get the exception message
                    request_method=http_method,
                    request_url=url,
                    request_data=json.dumps(data),
                )

        try:
            self.log.debug(
                "RES: {} : {} {} : {} {}".format(
                    description,
                    http_method,
                    url,
                    response.status_code,
                    json.dumps(response.json()),
                )
            )
        except ValueError:
            self.log.debug(
                "RES: {} : {} {} : {} {}".format(
                    description,
                    http_method,
                    url,
                    response.status_code,
                    response.text,
                )
            )

        return response

    @property
    def tenant(self):
        """Retrieve a reference to `.tenant.TenantController` object.

        See the class :py:class:`.tenant.TenantController` for the methods
        available.

        Example
        -------
        This example calls the method
        :py:meth:`list() <.tenant.TenantController.list>` in
        :py:class:`.tenant.TenantController`.

        >>> client = ContainerPlatformClient(...)
        >>> client.create_session()
        >>> client.tenant.list()
        """
        return self._tenant

    @property
    def config(self):
        """Retrieve a reference to `.config.ConfigController` object.

        See the class :py:class:`.config.ConfigController` for the methods
        available.

        Example
        -------
        This example calls the method
        :py:meth:`auth() <.config.ConfigController.auth>` in
        :py:class:`.config.ConfigController`.

        >>> client = ContainerPlatformClient(...)
        >>> client.create_session()
        >>> client.config.auth(
        ...        {
        ...            "external_identity_server":  {
        ...               "bind_pwd":"5ambaPwd@",
        ...                "user_attribute":"sAMAccountName",
        ...                "bind_type":"search_bind",
        ...                "bind_dn": (
        ...                     "cn=Administrator,CN=Users,DC=samdom,"
        ...                     "DC=example,DC=com"
        ...                     ),
        ...                "host":"10.1.0.77",
        ...                "security_protocol":"ldaps",
        ...                "base_dn":"CN=Users,DC=samdom,DC=example,DC=com",
        ...                "verify_peer": False,
        ...                "type":"Active Directory",
        ...                "port":636
        ...            }
        ...        }
        ...    )
        """  # noqa: E501
        return self._config

    @property
    def k8s_cluster(self):
        """Retrieve a reference to `.k8s_cluster.K8sClusterController` object.

        See the class :py:class:`.k8s_cluster.K8sClusterController` for the
        methods available.

        Example
        -------
        This example calls the method
        :py:meth:`list() <.k8s_cluster.K8sClusterController.list>` in
        :py:class:`.k8s_cluster.K8sClusterController`.

        >>> client = ContainerPlatformClient(...)
        >>> client.create_session()
        >>> client.k8s_cluster.list()
        """
        return self._k8s_cluster

    @property
    def k8s_worker(self):
        """Retrieve a reference to `.k8s_worker.K8sWorkerController` object.

        See the class :py:class:`.k8s_worker.K8sWorkerController` for the
        methods available.

        Example
        -------
        This example calls the method
        :py:meth:`list() <.k8s_worker.K8sWorkerController.list>` in
        :py:class:`.k8s_worker.K8sWorkerController`.

        >>> client = ContainerPlatformClient(...)
        >>> client.create_session()
        >>> client.k8s_worker.list()
        """
        return self._k8s_worker

    @property
    def gateway(self):
        """Retrieve a reference to `.gateway.GatewayController` object.

        See the class :py:class:`.gateway.GatewayController` for the methods
        available.

        Example
        -------
        This example calls the method
        :py:meth:`list() <.gateway.GatewayController.list>` in
        :py:class:`.gateway.GatewayController`.

        >>> client = ContainerPlatformClient(...)
        >>> client.create_session()
        >>> client.gateway.list()
        """
        return self._gateway

    @property
    def license(self):
        """Retrieve a reference to a `.license.LicenseController` object.

        See the class :py:class:`.license.LicenseController` for the methods
        available.

        Example
        -------
        This example calls the method
        :py:meth:`list() <.license.LicenseController.list>` in
        :py:class:`.license.LicenseController`.

        >>> client = ContainerPlatformClient(...)
        >>> client.create_session()
        >>> client.license.list()
        """
        return self._license

    @property
    def lock(self):
        """Retrieve a reference to a `.lock.LockController` object.

        See the class :py:class:`.lock.LockController` for the methods
        available.

        Example
        -------
        This example calls the method
        :py:meth:`get() <.lock.LockController.list>` in
        :py:class:`.lock.LockController`.

        >>> client = ContainerPlatformClient(...)
        >>> client.create_session()
        >>> client.lock.get()
        """
        return self._lock

    @property
    def log(self):
        """Retrieve a reference to a `:py:class:`.logger.Logger`.

        The log function can be
        called from controller objects via the `client` parameter passed in
        during instantiation of the controller.

        Example
        -------
        class K8sClusterController:
            ...

            def __init__(self, client):
                self.client = client

            def some_method(self):
                ...
                self.client.log.error("Some Error")
        """
        return self._log

    @property
    def user(self):
        """Retrieve a reference to a `.lock.LockController` object.

        See the class :py:class:`.lock.UserController` for the methods
        available.

        Example
        -------
        This example calls the method
        :py:meth:`get() <.user.UserController.get>` in
        :py:class:`.user.UserController`.

        >>> client = ContainerPlatformClient(...)
        >>> client.create_session()
        >>> client.user.get()
        """
        return self._user

    @property
    def catalog(self):
        """Retrieve a reference to a `.catalog.CatalogController` object.

        See the class :py:class:`.catalog.CatalogController` for the methods
        available.

        Example
        -------
        This example calls the method
        :py:meth:`create() <.catalog.CatalogController.create>` in
        :py:class:`.catalog.CatalogController`.

        >>> client = ContainerPlatformClient(...)
        >>> client.create_session()
        >>> client.catalog.create()
        """
        return self._catalog

    @property
    def role(self):
        """Retrieve a reference to a `.role.RoleController` object.

        See the class :py:class:`.role.RoleController` for the methods
        available.

        Example
        -------
        This example calls the method :py:meth:`get()
        <.role.RoleController.get>`
        in :py:class:`.role.RoleController`.

        >>> client = ContainerPlatformClient(...)
        >>> client.create_session()
        >>> client.role.get()
        """
        return self._role

    @property
    def datatap(self):
        """Retrieve a reference to a `.datatap.DatatapController` object.

        See the class :py:class:`.role.DatatapController` for the methods
        available.

        Example
        -------
        This example calls the method :py:meth:`get()
        <.datatap.DatatapController.get>`
        in :py:class:`.datatap.DatatapController`.

        >>> client = ContainerPlatformClient(...)
        >>> client.create_session()
        >>> client.datatap.get()
        """
        return self._datatap
