#!/usr/bin/env python3

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

"""HPE Container Platform CLI."""

from __future__ import print_function

import abc
import base64
import configparser
import json
import os
import sys
from collections import OrderedDict

import fire
import jmespath

from jinja2 import Environment
import six
import traceback
import yaml
import wrapt

from hpecp import (
    APIException,
    APIItemConflictException,
    ContainerPlatformClient,
    ContainerPlatformClientException,
)
from hpecp.k8s_worker import WorkerK8sStatus
from hpecp.logger import Logger
from hpecp.gateway import GatewayStatus
from hpecp.k8s_cluster import K8sClusterHostConfig, K8sClusterStatus
from hpecp.exceptions import APIItemNotFoundException, APIUnknownException
from textwrap import dedent
import inspect


if sys.version_info[0] >= 3:
    unicode = str

_log = Logger().get_logger(__file__)

PROFILE = os.getenv("PROFILE", "default",)

_log.debug(
    "PROFILE envirionment variable exists with value '{}'".format(PROFILE)
)

if "HPECP_CONFIG_FILE" in os.environ:
    HPECP_CONFIG_FILE = os.path.expandvars(os.getenv("HPECP_CONFIG_FILE"))
    _log.debug(
        "HPECP_CONFIG_FILE env variable exists with value '{}'".format(
            HPECP_CONFIG_FILE
        )
    )
else:
    HPECP_CONFIG_FILE = "~/.hpecp.conf"
    _log.debug(
        "HPECP_CONFIG_FILE env variable not found, setting to '{}'".format(
            HPECP_CONFIG_FILE
        )
    )


@wrapt.decorator
def intercept_exception(wrapped, instance, args, kwargs):
    """Handle Exceptions."""

    def _handle_unknown_exception():
        """Handle unknoen exceptions."""
        if _log.level == "DEBUG":
            print(
                "Unknown error.", file=sys.stderr,
            )
        else:
            print(
                "Unknown error. To debug run with env var LOG_LEVEL=DEBUG",
                file=sys.stderr,
            )
        tb = traceback.format_exc()
        _log.debug(tb)
        sys.exit(1)

    try:
        return wrapped(*args, **kwargs)
    except AssertionError as ae:
        print(ae, file=sys.stderr)
        sys.exit(1)
    except APIUnknownException:
        _handle_unknown_exception()
    except (
        APIException,
        APIItemNotFoundException,
        ContainerPlatformClientException,
    ) as e:
        print(e.message, file=sys.stderr)
        sys.exit(1)
    except Exception:
        _handle_unknown_exception()


@intercept_exception
def get_client(start_session=True):
    """Retrieve a reference to an authenticated client object."""
    client = ContainerPlatformClient.create_from_config_file(
        config_file=HPECP_CONFIG_FILE, profile=PROFILE,
    )
    if start_session:
        client.create_session()
    return client


@six.add_metaclass(abc.ABCMeta)
class BaseProxy:
    """Base 'proxy' class for generic calls to API."""

    def new_instance(self, client_module_name):
        """Create a new instance (constructor).

        Parameters
        ----------
        client_module_name : str
            Name of the property in the ContainerPlatformClient that
            points to the different modules (user, gateway, cluster, etc)
        """
        self.client_module_name = client_module_name
        super(BaseProxy, self).__init__()

    def all_fields(self):
        """Retrieve Entity columns."""
        try:
            # contstruct a dummy client to retrieve the
            # field metadata
            dummy_client = ContainerPlatformClient(
                api_host="127.0.0.1",
                api_port=8080,
                use_ssl=False,
                verify_ssl=False,
                warn_ssl=False,
                username="dummyuser",
                password="dummypassword",
            )
            self.client_module_property = getattr(
                dummy_client, self.client_module_name
            )
            return getattr(
                self.client_module_property, "resource_class"
            ).all_fields
        except Exception:
            return []

    @intercept_exception
    def get(self, id, output="yaml", params=None):
        """Retrieve a Resource by ID.

        id: string
            the id of the resource with format: '/api/path/[0-9]+'
        output: string
            how to display the output, either 'yaml' or 'json', default 'yaml'
        """
        self.client = get_client()
        self.client_module_property = getattr(
            self.client, self.client_module_name
        )
        response = self.client_module_property.get(id=id, params=params)

        if output == "yaml":
            print(
                yaml.dump(
                    yaml.load(
                        json.dumps(response.json), Loader=yaml.FullLoader,
                    )
                )
            )
        else:
            print(json.dumps(response.json))

    @intercept_exception
    def delete(
        self, id,
    ):
        """Delete a resource.

        :param id: the resource ID
        """
        self.client = get_client()
        self.client_module_property = getattr(
            self.client, self.client_module_name
        )
        self.client_module_property.delete(id=id)

    @intercept_exception
    def list(self, output="table", columns=all_fields, query={}):
        """Retrieve the list of resources.

        Parameters
        ----------
        output : str, optional
            Define how the output should be printed, by default "json"
        columns : list/tuple, optional
            List of specific columns to be displayed, by default []
            `Catalog.default_display_fields`
        query : dict, optional
            Query in jmespath (https://jmespath.org/) format, by default {}
        """
        if columns is [] and query is {}:
            print(
                "You must only provide '--columns' OR '--query' parameters.",
                file=sys.stderr,
            )
            sys.exit(1)

        self.client = get_client()
        self.client_module_property = getattr(
            self.client, self.client_module_name
        )

        # use tabulate for simplified user output
        if len(query) == 0:
            if output not in ["table", "text"]:
                print(
                    "When --columns param = [], the --output param must be"
                    " 'table' or 'text'",
                    file=sys.stderr,
                )
                sys.exit(1)

            if output == "table":
                print(
                    self.client_module_property.list().tabulate(
                        columns=columns
                    )
                )
            else:
                print(
                    self.client_module_property.list().tabulate(
                        columns=columns, style="plain", display_headers=False
                    )
                )

        # user has provided a jmes query
        else:
            if output not in ["json"]:
                print(
                    "If you provide a jmes query, the output must be 'json'",
                    file=sys.stderr,
                )
                sys.exit(1)

            data = self.client_module_property.list().json
            print(json.dumps(jmespath.search(str(query), data)))

    def wait_for_state(
        self, id, states=[], timeout_secs=60,
    ):
        """See wait_for_status()."""
        self.wait_for_status(id, states, timeout_secs)

    def wait_for_status(
        self, id, status=[], timeout_secs=60,
    ):
        """Wait for resource to have one or more statuses.

        :param id: Resource id with format: /api/path/[0-9]+
        :param status: status(es) to wait for with format:
            ['status1', 'status2', 'statusn']
        :param timeout_secs: how many secs to wait before exiting
        :returns True/False if status was found within timeout_secs. May
            raise APIException.
        """
        self.client = get_client()
        self.client_module_property = getattr(
            self.client, self.client_module_name
        )

        resource_status = [
            self.client_module_property.status_class[s] for s in status
        ]

        _log.debug("resource_status = {}".format(resource_status))

        try:
            success = self.client_module_property.wait_for_status(
                id=id, status=resource_status, timeout_secs=timeout_secs,
            )
        except Exception:
            success = False

        if not success:
            print(
                "Failed to reach state(s) {} in {}s".format(
                    str(status), str(timeout_secs),
                ),
                file=sys.stderr,
            )
            sys.exit(1)

    def wait_for_delete(
        self, id, timeout_secs=1200,
    ):
        """Wait for Gateway to be deleted.

        :param id: Cluster id with format: /api/v1/workers/[0-9]+
        :param timeout_secs: how many secs to wait before exiting
        :returns True if gateway was deleted within timeout_secs.
        """
        self.wait_for_state(
            id=id, timeout_secs=timeout_secs,
        )


class CatalogProxy(BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.catalog>`."""

    def __init__(self):
        """Initiate this proxy class with the client module name."""
        super(CatalogProxy, self).new_instance("catalog")

    def __dir__(self):
        """Return the CLI method names."""
        return [
            "get",
            "list",
            "delete",
            "wait_for_state",
            "refresh",
            "install",
        ]

    def delete(self, id):
        """Not implemented."""
        raise AttributeError("'CatalogProxy' object has no attribute 'delete'")

    def refresh(self, catalog_id):
        """Refresh a catalog.

        Parameters
        ----------
        catalog_id : str
            The ID of the catalog - format: '/api/v1/catalog/[0-9]+'

        Examples
        --------
        > hpecp catalog refresh /api/v1/catalog/99

        """
        try:
            get_client().catalog.refresh(catalog_id)

            # TODO: Report progress of the refresh workflow
        except AssertionError as ae:
            print(ae, file=sys.stderr)
            sys.exit(1)
        except (APIException, APIItemNotFoundException) as e:
            print(e.message, file=sys.stderr)
            sys.exit(1)

    def install(self, catalog_id):
        """Install a catalog.

        Parameters
        ----------
        catalog_id : str
            The ID of the catalog - format: '/api/v1/catalog/[0-9]+'

        Examples
        --------
        > hpecp catalog install /api/v1/catalog/99

        """
        try:
            get_client().catalog.install(catalog_id)

            # TODO: Implement a way to check if the installation is actually
            # successful (and maybe report progress?) - wait_for_state()?
        except AssertionError as ae:
            print(ae, file=sys.stderr)
            sys.exit(1)
        except (APIException, APIItemNotFoundException) as e:
            print(e.message, file=sys.stderr)
            sys.exit(1)


class GatewayProxy(BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.gateway>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return [
            "create_with_ssh_key",
            "delete",
            "get",
            "list",
            "states",
            "wait_for_state",
        ]

    def __init__(self):
        """Initiate this proxy class with the client module name."""
        super(GatewayProxy, self).new_instance("gateway")

    @intercept_exception
    def create_with_ssh_key(
        self,
        ip,
        proxy_node_hostname,
        ssh_key=None,
        ssh_key_file=None,
        tags=[],
    ):
        """Create a Gateway using SSH key authentication.

        Parameters
        ----------
        ip : string
            The IP address of the proxy host.  Used for internal
            communication.
        proxy_node_hostname: string
            Clients will access cluster services will be accessed
            using this name.
        ssh_key: string
            The ssh key data as a string.  Alternatively, use the
            ssh_key_file parameter.
        ssh_key_file: string
            The file path to the ssh key.  Alternatively, use the
            ssh_key parameter.
        tags: string
            Tags to add to the gateway, for example:
            "{ 'tag1': 'foo', 'tag2', 'bar' }".
        """
        if ssh_key is None and ssh_key_file is None:
            print(
                "Either ssh_key or ssh_key_file must be provided",
                file=sys.stderr,
            )
            sys.exit(1)

        if ssh_key is not None and ssh_key_file is not None:
            print(
                "Either ssh_key or ssh_key_file must be provided",
                file=sys.stderr,
            )
            sys.exit(1)

        if ssh_key_file:
            with open(ssh_key_file) as f:
                ssh_key = f.read()

        gateway_id = get_client().gateway.create_with_ssh_key(
            ip=ip,
            proxy_node_hostname=proxy_node_hostname,
            ssh_key_data=ssh_key,
            tags=tags,
        )
        print(gateway_id)

    def states(self,):
        """Return a list of valid states."""
        print([s.name for s in GatewayStatus])


class K8sWorkerProxy(BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.k8s_worker>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return [
            "create_with_ssh_key",
            "delete",
            "get",
            "list",
            "set_storage",
            "statuses",
            "wait_for_status",
        ]

    def __init__(self):
        """Initiate this proxy class with the client module name."""
        super(K8sWorkerProxy, self).new_instance("k8s_worker")

    @intercept_exception
    def create_with_ssh_key(
        self, ip=None, ssh_key=None, ssh_key_file=None, tags=[],
    ):
        """Create a K8s Worker using SSH key authentication.

        Parameters
        ----------
        ip : str, optional
            The IP address of the host, this is used for internal
            communication, by default None.
        ssh_key : str, optional
            The SSH key data as a string, instead of this location to a key
            file may also be provided, by default None.
        ssh_key_file : str, optional
            The SSH key file path, by default None
        tags : list, optional
            Tags to use, e.g. "{ "tag1": "foo", "tag2": "bar"}", by default []
        """
        if ssh_key is None and ssh_key_file is None:
            print(
                "Either ssh_key or ssh_key_file must be provided",
                file=sys.stderr,
            )
            sys.exit(1)

        if ssh_key is not None and ssh_key_file is not None:
            print(
                "Either ssh_key or ssh_key_file must be provided",
                file=sys.stderr,
            )
            sys.exit(1)

        if ssh_key_file:
            with open(ssh_key_file) as f:
                ssh_key = f.read()

        worker_id = get_client().k8s_worker.create_with_ssh_key(
            ip=ip, ssh_key_data=ssh_key, tags=tags,
        )
        print(worker_id)

    # TODO: verify with engineering if setup_log is a valid parameter
    # def get(self, id, setup_log=False):
    #     """Get a K8SWorker."""
    #     if setup_log is True:
    #         params = {"setup_log": "true"}
    #     else:
    #         params = {}
    #     return super(K8sWorkerProxy, self).get(id=id, params=params)

    @intercept_exception
    def set_storage(
        self, id, ephemeral_disks, persistent_disks=None,
    ):
        """Set storage for a k8s worker.

        Parameters
        ----------
        id : str
            The k8s worker ID
        ephemeral_disks : str
            Comma separated string containing ephemeral disks.
            e.g: "/dev/nvme2n1,/dev/nvme2n2"
        persistent_disks : str, optional
            Comma separated string containing persistent disks, by default
            None.
            e.g: "/dev/nvme1n1,/dev/nvme1n2"
        """
        if not ephemeral_disks:
            print("'ephemeral_disks' must be provided", file=sys.stderr)
            sys.exit(1)

        p_disks = (
            persistent_disks.split(",") if persistent_disks is not None else []
        )
        e_disks = ephemeral_disks.split(",")

        get_client().k8s_worker.set_storage(
            worker_id=id, persistent_disks=p_disks, ephemeral_disks=e_disks,
        )

    def statuses(self,):
        """Return a list of valid statuses."""
        print([s.name for s in WorkerK8sStatus])


class K8sClusterProxy(BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.k8s_cluster>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return [
            "admin_kube_config",
            "create",
            "dashboard_url",
            "dashboard_token",
            "delete",
            "get",
            "k8s_supported_versions",
            "list",
            "statuses",
            "wait_for_status",
        ]

    def __init__(self):
        """Initiate this proxy class with the client module name."""
        super(K8sClusterProxy, self).new_instance("k8s_cluster")

    @intercept_exception
    def create(
        self,
        name,
        k8shosts_config,
        description=None,
        k8s_version=None,
        pod_network_range="10.192.0.0/12",
        service_network_range="10.96.0.0/12",
        pod_dns_domain="cluster.local",
        persistent_storage_local=False,
        persistent_storage_nimble_csi=False,
    ):
        """Create a K8s Cluster.

        :param name: the cluster name
        :param k8shosts_config: k8s host ids and roles 'id1:master|worker,id2:
            master|worker,...'
        :param description: the cluster descripton
        :param k8s_version: e.g. 1.17.0
        :param pod_network_range: the pod network range,
            default='10.192.0.0/12'
        :param service_network_range: the service network range,
            default='10.96.0.0/12'
        :param pod_dns_domain: the pod dns domain, default='cluster.local'
        :param persistent_storage_local: True/False
        :param persistent_storage_nimble_csi: True/False
        """
        host_config = [
            K8sClusterHostConfig.create_from_list(h.split(":"))
            for h in k8shosts_config.split(",")
        ]

        print(
            get_client().k8s_cluster.create(
                name=name,
                description=description,
                k8s_version=k8s_version,
                pod_network_range=pod_network_range,
                service_network_range=service_network_range,
                pod_dns_domain=pod_dns_domain,
                persistent_storage_local=persistent_storage_local,
                persistent_storage_nimble_csi=persistent_storage_nimble_csi,
                k8shosts_config=host_config,
            )
        )

    def admin_kube_config(self, id):
        """Retrieve a K8s Cluster Admin Kube Config.

        :param id: the cluster ID
        """
        print(
            get_client()
            .k8s_cluster.get(id)
            .admin_kube_config.replace("\\n", "\n",)
        )

    def dashboard_url(
        self, id,
    ):
        """Retrieve a K8s Cluster Dashboard URL.

        :param id: the cluster ID
        """
        url = get_client().k8s_cluster.get(id=id).dashboard_endpoint_access
        print(url)

    def dashboard_token(
        self, id,
    ):
        """Retrieve a K8s Cluster Dashboard Token.

        :param id: the cluster ID
        """
        token = get_client().k8s_cluster.get(id=id).dashboard_token
        if six.PY2:
            print(base64.b64decode(token.encode()))
        else:
            print(base64.b64decode(token.encode()).decode("utf-8"))

    def statuses(self,):
        """Return a list of valid statuses."""
        print([s.name for s in K8sClusterStatus])

    def k8s_supported_versions(
        self,
        output="json",
        major_filter=None,
        minor_filter=None,
        patch_filter=None,
    ):
        """Print a list of supported k8s versions.

        :param output: how to print the output, 'json' or 'text'
        :param major_filter: only return versions matching major_filter
        :param minor_filter: only return versions matching minor_filter
        :param patch_filter: only return versions matching patch_filter

        Example::

        hpecp k8scluster k8s_supported_versions --major-filter 1
            --minor-filter 17
        """
        if output not in [
            "json",
            "text",
        ]:
            print(
                "'output' parameter ust be 'json' or 'text'", file=sys.stderr
            )
            sys.exit(1)

        if major_filter is not None and not isinstance(major_filter, int):
            print("'major_filter' if provided must be an int", file=sys.stderr)
            sys.exit(1)

        if minor_filter is not None and not isinstance(minor_filter, int):
            print("'minor_filter' if provided must be an int", file=sys.stderr)
            sys.exit(1)

        if patch_filter is not None and not isinstance(patch_filter, int):
            print("'patch_filter' if provided must be an int", file=sys.stderr)
            sys.exit(1)

        if major_filter:
            major_filter = int(major_filter)

        if minor_filter:
            minor_filter = int(minor_filter)

        if patch_filter:
            patch_filter = int(patch_filter)

        vers = []
        for v in get_client().k8s_cluster.k8s_supported_versions():
            (major, minor, patch) = v.split(".")
            major = int(major)
            minor = int(minor)
            patch = int(patch)
            if (
                (major_filter is not None and major != major_filter)
                or (minor_filter is not None and minor != minor_filter)
                or (patch_filter is not None and patch != patch_filter)
            ):
                continue
            else:
                vers.append(v)

        if output == "json":
            print(vers)
        else:
            print(" ".join(vers))


class LockProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.lock>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return [
            "create",
            "delete",
            "delete_all",
            "list",
        ]

    def list(
        self, output="yaml",
    ):
        """Get the system and user locks.

        :param output: how to display the output ['yaml'|'json']
        """
        if output not in ["yaml", "json"]:
            print(
                "'output' parameter must be 'yaml' or 'json'", file=sys.stderr
            )
            sys.exit(1)

        response = get_client().lock.get()

        if output == "yaml":
            print(
                yaml.dump(
                    yaml.load(json.dumps(response), Loader=yaml.FullLoader,)
                )
            )
        else:
            print(json.dumps(response))

    @intercept_exception
    def create(
        self, reason,
    ):
        """Create a lock."""
        print(get_client().lock.create(reason), file=sys.stdout)

    @intercept_exception
    def delete(
        self, id,
    ):
        """Delete a user lock."""
        get_client().lock.delete(id)

    @intercept_exception
    def delete_all(
        self, timeout_secs=300,
    ):
        """Delete all locks."""
        success = get_client().lock.delete_all(timeout_secs=timeout_secs)
        if not success:
            print("Could not delete locks.", file=sys.stderr)
            sys.exit(1)


class LicenseProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.license>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return ["delete", "delete_all", "list", "platform_id", "register"]

    @intercept_exception
    def platform_id(self,):
        """Get the platform ID."""
        print(get_client().license.platform_id())

    def list(
        self, output="yaml", license_key_only=False,
    ):
        """Retrieve the list of licenses.

        :param output: how to display the output ['yaml'|'json']
        """
        response = get_client().license.list()
        if license_key_only:
            response = [
                str(unicode(li["LicenseKey"])) for li in response["Licenses"]
            ]
            print("\n".join(response))
        else:
            if output == "yaml":
                print(
                    yaml.dump(
                        yaml.load(
                            json.dumps(response), Loader=yaml.FullLoader,
                        )
                    )
                )
            else:
                print(json.dumps(response))

    @intercept_exception
    def register(
        self, server_filename,
    ):
        """Register a license.

        :param server_filename: Filepath to the license on the server, e.g.
            '/srv/bluedata/license/LICENSE-1.txt'
        """
        print(get_client().license.register(server_filename=server_filename))

    # TODO implement me!
    # def upload_with_ssh_key(
    #     self,
    #     server_filename,
    #     ssh_key_file=None,
    #     ssh_key_data=None,
    #     license_file=None,
    #     base64enc_license_data=None,
    # ):
    #     """Not implemented yet.

    #     Workaround:
    #     -----------
    #      - scp your license to '/srv/bluedata/license/' on the controller
    #      - run client.license.register(server_filename) to register
    #        the license
    #     """
    #     raise Exception(
    #         "Not implemented yet! Workaround: scp your license to"
    #         "'/srv/bluedata/license/'"
    #     )

    # TODO implement me!
    # def upload_with_ssh_pass(
    #     self,
    #     server_filename,
    #     ssh_username,
    #     ssh_password,
    #     license_file=None,
    #     base64enc_license_data=None,
    # ):
    #     """Not implemented yet.

    #     Workaround:
    #     -----------
    #      - scp your license to '/srv/bluedata/license/' on the controller
    #      - run client.license.register(server_filename) to register
    #        the license
    #     """
    #     raise Exception(
    #         "Not implemented yet! Workaround: scp your license to"
    #         "'/srv/bluedata/license/'"
    #     )

    def delete(
        self, license_key,
    ):
        """Delete a license by LicenseKey.

        :param license_key: The license key, e.g. '1234 1234 ... 1234
            "SOMETEXT"'
        """
        get_client().license.delete(license_key=license_key)
        print("Delete submitted - verify with: `hpecp license list`")

    def delete_all(self,):
        """Delete all licenses."""
        response = get_client().license.list()
        all_license_keys = [
            str(unicode(li["LicenseKey"])) for li in response["Licenses"]
        ]
        for licence_key in all_license_keys:
            get_client().license.delete(license_key=licence_key)
        print("Delete submitted - verify with: `hpecp license list`")


class HttpClientProxy(object):
    """Proxy object to :py:attr:`<hpecp.client._request>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return ["delete", "get", "post", "put"]

    @intercept_exception
    def get(
        self, url,
    ):
        """Make HTTP GET request.

        Examples
        --------
        $ hpecp httpclient get /api/v1/workers
        """
        response = get_client()._request(
            url, http_method="get", description="CLI HTTP GET",
        )
        print(response.text, file=sys.stdout)

    @intercept_exception
    def delete(
        self, url,
    ):
        """Make HTTP DELETE request.

        Examples
        --------
        $ hpecp httpclient delete /api/v1/workers/1
        """
        get_client()._request(
            url, http_method="delete", description="CLI HTTP DELETE",
        )

    @intercept_exception
    def post(
        self, url, json_file="",
    ):
        """Make HTTP POST request.

        Examples
        --------
        $ cat > my.json <<-EOF
            {
                "external_identity_server":  {
                    "bind_pwd":"5ambaPwd@",
                    "user_attribute":"sAMAccountName",
                    "bind_type":"search_bind",
                    "bind_dn":"cn=Administrator,CN=Users,DC=samdom,DC=example,DC=com",
                    "host":"10.1.0.77",
                    "security_protocol":"ldaps",
                    "base_dn":"CN=Users,DC=samdom,DC=example,DC=com",
                    "verify_peer": false,
                    "type":"Active Directory",
                    "port":636
                }
            }
            EOF

            hpecp httpclient post /api/v2/config/auth --json-file my.json
        """
        with open(json_file, "r",) as f:
            data = json.load(f)

        response = get_client()._request(
            url, http_method="post", data=data, description="CLI HTTP POST",
        )
        print(response.text, file=sys.stdout)

    @intercept_exception
    def put(
        self, url, json_file="",
    ):
        """Make HTTP PUT request.

        Examples
        --------
        $ hpecp httpclient put /api/v2/config/auth --json-file my.json
        """  # noqa: W293
        with open(json_file, "r",) as f:
            data = json.load(f)

        response = get_client()._request(
            url, http_method="put", data=data, description="CLI HTTP PUT",
        )
        print(response.text, file=sys.stdout)


class UserProxy(BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.user>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return ["create"]

    def __init__(self):
        """Initiate this proxy class with the client module name."""
        super(UserProxy, self).new_instance("user")

    def create(
        self, name, description, is_external=False,
    ):
        """Create a User.

        :param name: the user name
        :param description: the user descripton

        """
        try:
            user_id = get_client().user.create(
                name=name, description=description, is_external=is_external,
            )
            print(user_id)
        except APIItemConflictException:
            print("User already exists.")
            sys.exit(1)


class RoleProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.role>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return ["get"]

    def get(
        self, role_id, output="yaml",
    ):
        """Retrieve a Role by Id.

        :param role_id: the id of the role with format: '/api/v1/role/[0-9]+'
        :param output: how to display the output ['yaml'|'json']
        """
        response = get_client().role.get(role_id)
        if output == "yaml":
            print(
                yaml.dump(
                    yaml.load(
                        json.dumps(response.json), Loader=yaml.FullLoader,
                    )
                )
            )
        else:
            print(response.json)


def configure_cli():
    """Configure the CLI."""
    controller_api_host = None
    controller_api_port = None
    controller_use_ssl = None
    controller_verify_ssl = None
    controller_warn_ssl = None
    controller_username = None
    controller_password = None

    config_path = os.path.join(os.path.expanduser("~"), ".hpecp.conf",)

    if os.path.exists(config_path):
        config_reader = ContainerPlatformClient.create_from_config_file()
        controller_api_host = config_reader.api_host
        controller_api_port = config_reader.api_port
        controller_use_ssl = config_reader.use_ssl
        controller_verify_ssl = config_reader.verify_ssl
        controller_warn_ssl = config_reader.warn_ssl
        controller_username = config_reader.username
        controller_password = config_reader.password

    sys.stdout.write("Controller API Host [{}]: ".format(controller_api_host))
    tmp = six.moves.input()
    if tmp != "":
        controller_api_host = tmp

    sys.stdout.write("Controller API Port [{}]: ".format(controller_api_port))
    tmp = six.moves.input()
    if tmp != "":
        controller_api_port = tmp

    sys.stdout.write(
        "Controller uses ssl (True|False) [{}]: ".format(controller_use_ssl)
    )
    tmp = six.moves.input()
    if tmp != "":
        controller_use_ssl = tmp

    sys.stdout.write(
        "Controller verify ssl (True|False) [{}]: ".format(
            controller_verify_ssl
        )
    )
    tmp = six.moves.input()
    if tmp != "":
        controller_verify_ssl = tmp

    sys.stdout.write(
        "Controller warn ssl (True|False) [{}]: ".format(controller_warn_ssl)
    )
    tmp = six.moves.input()
    if tmp != "":
        controller_warn_ssl = tmp

    sys.stdout.write("Controller Username [{}]: ".format(controller_username))
    tmp = six.moves.input()
    if tmp != "":
        controller_username = tmp

    sys.stdout.write("Controller Password [{}]: ".format(controller_password))
    tmp = six.moves.input()
    if tmp != "":
        controller_password = tmp

    config = configparser.ConfigParser()
    config["default"] = OrderedDict()
    config["default"]["api_host"] = controller_api_host
    config["default"]["api_port"] = str(controller_api_port)
    config["default"]["use_ssl"] = str(controller_use_ssl)
    config["default"]["verify_ssl"] = str(controller_verify_ssl)
    config["default"]["warn_ssl"] = str(controller_warn_ssl)
    config["default"]["username"] = controller_username
    config["default"]["password"] = controller_password

    with open(config_path, "w") as config_file:
        config.write(config_file)


class AutoComplete:
    """Shell autocompletion scripts.

    Example Usage:

    hpecp autocomplete bash > hpecp-bash.sh && source hpecp-bash.sh
    """

    def __dir__(self):
        """Return the CLI method names."""
        return ["bash"]

    def __init__(self, cli):
        """Create AutoCompletion class instance.

        Parameters
        ----------
        cli : CLI
            the owning cli instance
        """
        self.cli = cli

    def _get_metadata(self):

        modules = {}
        columns = {}
        for module_name in self.cli.__dict__.keys():

            # we manually define autocomplete for these methods
            if module_name in ["autocomplete", "configure_cli"]:
                continue

            module = getattr(self.cli, module_name)
            function_names = dir(module)

            try:
                all_fields = getattr(module, "all_fields")()
            except Exception:
                all_fields = []

            function_parameters = {}
            for function_name in function_names:
                function = getattr(module, function_name)

                if six.PY2:
                    parameter_names = list(inspect.getargspec(function).args)
                else:
                    parameter_names = list(
                        inspect.getfullargspec(function).args
                    )

                # parameter_names = list(function.__code__.co_varnames)
                if "self" in parameter_names:
                    parameter_names.remove("self")

                # prefix parameter names with '--'
                parameter_names = list(map("--".__add__, parameter_names))
                function_parameters.update({function_name: parameter_names})

            modules[module_name] = function_parameters
            columns[module_name] = all_fields

            # _log.debug(modules)
            # _log.debug(columns)

        return (modules, columns)

    def bash(self,):
        """Create autocompletion script for bash."""
        __bash_template = dedent(
            """\
            _hpecp_complete()
                {
                local cur prev BASE_LEVEL

                COMPREPLY=()
                cur=${COMP_WORDS[COMP_CWORD]}
                prev=${COMP_WORDS[COMP_CWORD-1]}

                COMP_WORDS_AS_STRING=$(IFS=, ; echo "${COMP_WORDS[*]}")

                case "$COMP_WORDS_AS_STRING" in

                {#
                    Example module dict:

                    {
                        'catalog': {
                        'delete': ['--id'],
                        'get': ['--id', '--output', '--response', '--e'],
                        'install': ['--catalog_id', '--ae', '--e'],
                        'list': ['--output', '--columns', '--query', '--data'],
                        'refresh': ['--catalog_id', '--ae', '--e'],
                        'wait_for_state': ['--id', '--states', '--timeout_secs']
                        }
                    }

                    Example columns dict:

                    {'catalog': ('label_name', 'label_description',  ...}
                #}

                {% set module_names = " ".join(modules.keys()) %}

                {% for module_name in modules %} {# e.g. 'catalog' #}

                    {% set function_names = " ".join(modules[module_name].keys()) %}

                    {% for function_name in modules[module_name] %}  {# e.g. mod = 'delete' #}

                        {% set param_names = " ".join(modules[module_name][function_name]).replace('_', '-') %}

                        {% for param_name in modules[module_name][function_name] %}
                            {% if param_name == "--columns" %}
                                {% set column_names = " ".join(columns[module_name]) %}
                    *"hpecp,{{module_name}},{{function_name}},{{param_name}}"*)
                        COMPREPLY=( $(compgen -W "{{column_names}} {{param_names}}" -- $cur) )
                        ;;
                            {% endif %}
                        {% endfor %}

                    *"hpecp,{{module_name}},{{function_name}}"*)

                        # we should be able to replace the above case statement with:
                        #
                        # if last parameter is "--columns"
                        # COMPREPLY=( $(compgen -W "{{column_names}}" -- $cur) )
                        # else
                        # COMPREPLY=( $(compgen -W "{{param_names}}" -- $cur) )
                        # fi

                        COMPREPLY=( $(compgen -W "{{param_names}}" -- $cur) )
                        ;;
                    {% endfor %}

                    *"hpecp,{{module_name}}"*)
                        COMPREPLY=( $(compgen -W "{{ function_names }}" -- $cur) )
                        ;;
                {% endfor %}

                    *"hpecp,autocomplete,bash"*)
                        COMPREPLY=( )
                        ;;
                    *"hpecp,autocomplete"*)
                        COMPREPLY=( $(compgen -W "bash" -- $cur) )
                        ;;
                    *"hpecp"*)
                        COMPREPLY=( $(compgen -W "autocomplete configure-cli {{  module_names }}" -- $cur) )
                    ;;

                esac

                return 0

            } &&
            complete -F _hpecp_complete hpecp
        """  # noqa: E501
        )

        (modules, columns) = self._get_metadata()

        print(
            Environment()
            .from_string(__bash_template)
            .render(modules=modules, columns=columns),
            file=sys.stdout,
        )


class CLI(object):
    """Command Line Interface for the HPE Container Platform."""

    def __dir__(self):
        """Return modules names."""
        return vars(self)

    def __init__(self,):
        """Create a CLI instance."""
        self.autocomplete = AutoComplete(self)
        self.configure_cli = configure_cli
        self.catalog = CatalogProxy()
        self.k8sworker = K8sWorkerProxy()
        self.k8scluster = K8sClusterProxy()
        self.gateway = GatewayProxy()
        self.lock = LockProxy()
        self.license = LicenseProxy()
        self.httpclient = HttpClientProxy()
        self.user = UserProxy()
        self.role = RoleProxy()


if __name__ == "__main__":
    fire.Fire(CLI)
