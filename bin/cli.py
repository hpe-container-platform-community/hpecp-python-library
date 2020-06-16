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

import base64
import configparser
import json
import os
import sys
from collections import OrderedDict

import fire
import jmespath
import six
import yaml

from hpecp import (
    APIException,
    APIItemConflictException,
    ContainerPlatformClient,
    ContainerPlatformClientException,
)
from hpecp.catalog import Catalog
from hpecp.exceptions import APIItemNotFoundException
from hpecp.gateway import Gateway, GatewayStatus
from hpecp.k8s_cluster import K8sClusterHostConfig, K8sClusterStatus
from hpecp.k8s_worker import WorkerK8sStatus
from hpecp.logger import Logger
from hpecp.user import User

if sys.version_info[0] >= 3:
    unicode = str

_log = Logger().get_logger(__file__)

PROFILE = os.getenv("PROFILE", "default",)

_log.debug(
    "PROFILE envirionment variable exists with value '{}'".format(PROFILE)
)

if "HPECP_CONFIG_FILE" in os.environ:
    HPECP_CONFIG_FILE = os.getenv("HPECP_CONFIG_FILE")
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


def get_client():
    """Retrieve a reference to an authenticated client object."""
    try:
        client = ContainerPlatformClient.create_from_config_file(
            config_file=HPECP_CONFIG_FILE, profile=PROFILE,
        )
        client.create_session()
        return client
    except APIException as e:
        print(e.message)
        sys.exit(1)
    except ContainerPlatformClientException as e:
        print(e.message)
        sys.exit(1)


class CatalogProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.catalog>`."""

    def list(
        self, output="json", columns=Catalog.default_display_fields, query={}
    ):
        """Retrieve the list of catalogs

        Parameters
        ----------
        output : str, optional
            Define how the output should be printed, by default "json"
        columns : list/tuple, optional
            List of speicifc columns to be displayed, by default
            `Catalog.default_display_fields`
        query : dict, optional
            Query in jmespath (https://jmespath.org/) format, by default {}

        Examples
        ----------

        > hpecp catalog list --output text --query '[0].distro_id'

        bluedata/spark240juphub7xssl

        """
        if output == "table":
            print(get_client().catalog.list().tabulate(columns=columns))
        elif output == "text":
            print(
                get_client()
                .catalog.list()
                .tabulate(
                    columns=columns, style="plain", display_headers=False,
                )
            )
        else:
            data = get_client().catalog.list().json
            if query:
                print(json.dumps(jmespath.search(str(query), data)))
            else:
                print(data)

    def refresh(self, catalog_id):
        """Refresh a catalog

        Parameters
        ----------
        catalog_id : str
            The ID of the catalog - format: '/api/v1/catalog/[0-9]+'

        Examples
        ----------

        > hpecp catalog refresh /api/v1/catalog/99

        """
        try:
            get_client().catalog.refresh(catalog_id)

            # TODO: Report progress of the refresh workflow
        except (APIException, APIItemNotFoundException) as e:
            print(e.message)
            sys.exit(1)

    def install(self, catalog_id):
        """Install a catalog

        Parameters
        ----------
        catalog_id : str
            The ID of the catalog - format: '/api/v1/catalog/[0-9]+'

        Examples
        ----------

        > hpecp catalog install /api/v1/catalog/99
        """
        try:
            get_client().catalog.install(catalog_id)

            # TODO: Implement a way to check if the installation is actually
            # successful (and maybe report progress?)
        except (APIException, APIItemNotFoundException) as e:
            print(e.message)
            sys.exit(1)


class GatewayProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.gateway>`."""

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
            print("Either ssh_key or ssh_key_file must be provided")
            sys.exit(1)

        if ssh_key is not None and ssh_key_file is not None:
            print("Either ssh_key or ssh_key_file must be provided")
            sys.exit(1)

        if ssh_key_file is not None:
            with open(ssh_key_file) as f:
                ssh_key = f.read()

        try:
            gateway_id = get_client().gateway.create_with_ssh_key(
                ip=ip,
                proxy_node_hostname=proxy_node_hostname,
                ssh_key_data=ssh_key,
                tags=tags,
            )
            print(gateway_id)
        except APIItemConflictException:
            print("Gateway already exists.")
            sys.exit(1)

    def create_with_ssh_password(self,):
        """Not yet implemented."""
        raise NotImplementedError("Not yet implemented")

    def get(
        self, gateway_id, output="yaml",
    ):
        """Retrieve a Gateway by ID.

        gateway_id: string
            the id of the gateway with format: '/api/v1/workers/[0-9]+'
        output: string
            how to display the output, either 'yaml' or 'json'
        """
        response = get_client().gateway.get(gateway_id)
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

    def list(
        self, output="table", columns=Gateway.default_display_fields, query={}
    ):
        """Retrieve the list of Gateways.

        :param output: how to display the output [text|table|json]
        :param query: jmespath (https://jmespath.org/) query

        Example::

        > hpecp gateway list --output json --query '[0].ip'

        10.1.0.185

        > hpecp gateway list --output json --query
            '[*].[ip, purpose, state, hostname]'

        [['10.1.0.185', 'proxy', 'installed',
            'ip-10-1-0-185.us-west-2.compute.internal']]
        """  # noqa: W293
        if output == "table":
            print(get_client().gateway.list().tabulate(columns=columns))
        elif output == "text":
            print(
                get_client()
                .gateway.list()
                .tabulate(
                    columns=columns, style="plain", display_headers=False,
                )
            )
        else:
            data = get_client().gateway.list().json
            if query:
                print(json.dumps(jmespath.search(str(query), data)))
            else:
                print(data)

    def delete(
        self, gateway_id, wait_for_delete_secs=0,
    ):
        """Retrieve a Gateway by ID.

        gateway_id: string
            The id of the gateway with format: '/api/v1/workers/[0-9]+'
        wait_for_delete_secs: int
            For many secs to wait for the delete to happen.
            wait_for_delete_secs > 0 `calls wait_for_delete()`
            If 0 return immediately after calling delete.
        """
        try:
            get_client().gateway.delete(gateway_id)
        except APIException as e:
            print(e.message)
            sys.exit(1)

        if wait_for_delete_secs > 0:
            self.wait_for_delete(
                gateway_id=gateway_id, timeout_secs=wait_for_delete_secs,
            )

    def wait_for_delete(
        self, gateway_id, timeout_secs=1200,
    ):
        """Wait for Gateway to be deleted.

        :param gateway_id: Cluster id with format: /api/v1/workers/[0-9]+
        :param timeout_secs: how many secs to wait before exiting
        :returns True if gateway was deleted within timeout_secs.
        """
        self.wait_for_state(
            gateway_id=gateway_id, timeout_secs=timeout_secs,
        )

    def wait_for_state(
        self, gateway_id, states=[], timeout_secs=1200,
    ):
        """Wait for Gateway to have one or more statuses.

        :param gateway_id: Cluster id with format: /api/v1/workers/[0-9]+
        :param status: status(es) to wait for with format: ['status1',
            'status2', 'statusn'] - set to [] to wait for item to be deleted
        :param timeout_secs: how many secs to wait before exiting
        :returns True/False if status was found within timeout_secs. May raise
            APIException.

        See also: `hpecp gateway states`
        """
        gateway_states = [GatewayStatus[s] for s in states]

        try:
            success = get_client().gateway.wait_for_state(
                gateway_id=gateway_id, state=gateway_states,
            )
        except Exception:
            success = False

        if not success:
            print(
                "Failed to reach state(s) {} in {}".format(
                    str(states), str(timeout_secs),
                )
            )
            sys.exit(1)

    def states(self,):
        """Return a list of valid states."""
        print([s.name for s in GatewayStatus])


class K8sWorkerProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.k8s_worker>`."""

    def create_with_ssh_key(
        self, ip=None, ssh_key=None, ssh_key_file=None, tags=[],
    ):
        """Create a K8s Worker using SSH key authentication.

        :param ip: The IP address of the host.  Used for internal
            communication.
        :param ssh_key: The ssh key data as a string.  Alternatively, use the
            ssh_key_file parameter.
        :param ssh_key_file: The file path to the ssh key.  Alternatively, use
            the ssh_key parameter.
        :param tags: Tags to use, e.g. "{ 'tag1': 'foo', 'tag2', 'bar' }".
        """
        if ssh_key is None and ssh_key_file is None:
            print("Either ssh_key or ssh_key_file must be provided")
            sys.exit(1)

        if ssh_key is not None and ssh_key_file is not None:
            print("Either ssh_key or ssh_key_file must be provided")
            sys.exit(1)

        if ssh_key_file is not None:
            with open(ssh_key_file) as f:
                ssh_key_data = f.read()

        try:
            worker_id = get_client().k8s_worker.create_with_ssh_key(
                ip=ip, ssh_key_data=ssh_key_data, tags=tags,
            )
            print(worker_id)
        except APIItemConflictException:
            print("Worker already exists.")
            sys.exit(1)

    def create_with_ssh_password(self,):
        """Not yet implemented."""
        raise NotImplementedError("Not yet implemented")

    def list(
        self,
        all_columns=False,
        columns=["id", "description"],
        output="table",
        query={},
    ):
        """Display a table of K8s Workers.

        :param all_columns: (True/False) set to True to return all columns
        :param columns: (aaa) afadsfs
        :param output: how to display the output [text|table|json]
        :param query: jmespath (https://jmespath.org/) query

        Example::

        > hpecp k8sworker list --output json --query '[0].ip'
        10.1.0.185

        > hpecp k8sworker list --output json --query "[*].[status, hostname,
            ipaddr]"

        [['configured', 'ip-10-1-0-72.us-west-2.compute.internal', '10.1.0.72']
            ,['configured', 'ip-10-1-0-238.us-west-2.compute.internal',
            '10.1.0.238']]

        # Using jq to convert the json output to a table
        > hpecp k8sworker list --output json --query "[*].[status, hostname,
            ipaddr]" | jq -r '.[] | @csv'
        "configured","ip-10-1-0-72.us-west-2.compute.internal","10.1.0.72"
        "configured","ip-10-1-0-238.us-west-2.compute.internal","10.1.0.238"

        """  # noqa: W293
        if output == "table":
            print(get_client().k8s_worker.list().tabulate(columns=columns))
        elif output == "text":
            print(
                get_client()
                .k8s_worker.list()
                .tabulate(
                    columns=columns, style="plain", display_headers=False
                )
            )
        else:
            data = get_client().k8s_worker.list().json
            if query:
                print(json.dumps(jmespath.search(str(query), data)))
            else:
                print(data)

    def get(
        self, k8sworker_id,
    ):
        """Retrieve a K8s Worker.

        :param k8sworker_id: the worker ID
        """
        worker = get_client().k8s_worker.get(worker_id=k8sworker_id).json
        print(
            yaml.dump(yaml.load(json.dumps(worker), Loader=yaml.FullLoader,))
        )

    def delete(
        self, k8sworker_id,
    ):
        """Delete a K8s Worker.

        :param k8sworker_id: the worker ID
        """
        print(get_client().k8s_worker.delete(worker_id=k8sworker_id))

    def set_storage(
        self, k8sworker_id=None, persistent_disks=None, ephemeral_disks=None,
    ):
        """Set Storage for a K8S Worker.

        :param k8sworker_id: the worker ID
        :param persistent_disks: a comma separated list of zero or more
            persistent disks, e.g. "/dev/nvme2n1"
        :param ephemeral_disks: a comma separated list of zero or more
            ephemeral_disks disks, e.g. "/dev/nvme1n1"
        """
        p_disks = persistent_disks.split(",")
        e_disks = ephemeral_disks.split(",")

        get_client().k8s_worker.set_storage(
            worker_id=k8sworker_id,
            persistent_disks=p_disks,
            ephemeral_disks=e_disks,
        )

    def wait_for_status(
        self, worker_id, status=[], timeout_secs=1200,
    ):
        """Wait for Worker to have one or more statuses.

        :param worker_id: Worker id with format: /api/v1/workers/[0-9]+
        :param status: status(es) to wait for with format: ['status1',
            'status2', 'statusn'] - set to [] to wait for item to be deleted
        :param timeout_secs: how many secs to wait before exiting
        :returns True/False if status was found within timeout_secs. May raise
            APIException.

        See also: `hpecp k8sworker states`
        """
        worker_statuses = [WorkerK8sStatus[s] for s in status]

        client = get_client()
        try:
            success = client.k8s_worker.wait_for_status(
                worker_id=worker_id,
                status=worker_statuses,
                timeout_secs=timeout_secs,
            )
        except Exception as e:
            client.log.debug(e)
            success = False

        if not success:
            print(
                "Failed to reach state(s) {} in {}".format(
                    str(status), str(timeout_secs),
                )
            )
            sys.exit(1)

    def statuses(self,):
        """Return a list of valid statuses."""
        print([s.name for s in WorkerK8sStatus])


class K8sClusterProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.k8s_cluster>`."""

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

    def list(
        self,
        all_columns=False,
        columns=["id", "name", "description", "status"],
        output="table",
        query={},
    ):
        """Print a table of K8s Clusters.

        :param all_columns: (True/False) set to True to return all columns
        :param output: how to display the output [text|table]
        :param columns: Which columns to display

        Example
        -------
        $ hpecp k8scluster list --query "[*]._links.self.href | join(' ', @)" | tr -d '"'
        /api/v2/k8scluster/1 /api/v2/k8scluster/2
        """  # noqa: E501
        if all_columns:
            print(get_client().k8s_cluster.list().tabulate())
        else:
            if query:
                data = get_client().k8s_cluster.list().json
                print(json.dumps(jmespath.search(str(query), data)))
            else:
                print(
                    get_client().k8s_cluster.list().tabulate(columns=columns)
                )

    def get(
        self, k8scluster_id,
    ):
        """Retrieve a K8s Cluster.

        :param k8scluster_id: the cluster ID
        """
        response = (
            get_client().k8s_cluster.get(k8scluster_id=k8scluster_id).json
        )
        print(
            yaml.dump(yaml.load(json.dumps(response), Loader=yaml.FullLoader,))
        )

    def admin_kube_config(
        self, k8scluster_id,
    ):
        """Retrieve a K8s Cluster Admin Kube Config.

        :param k8scluster_id: the cluster ID
        """
        cfg = (
            get_client()
            .k8s_cluster.get(k8scluster_id=k8scluster_id)
            .json["admin_kube_config"]
        )
        print(cfg.replace("\\n", "\n",))

    def dashboard_url(
        self, k8scluster_id,
    ):
        """Retrieve a K8s Cluster Dashboard URL.

        :param k8scluster_id: the cluster ID
        """
        url = (
            get_client()
            .k8s_cluster.get(k8scluster_id=k8scluster_id)
            .json["dashboard_endpoint_access"]
        )
        print(url)

    def dashboard_token(
        self, k8scluster_id,
    ):
        """Retrieve a K8s Cluster Dashboard Token.

        :param k8scluster_id: the cluster ID
        """
        token = (
            get_client()
            .k8s_cluster.get(k8scluster_id=k8scluster_id)
            .json["dashboard_token"]
        )
        print(base64.b64decode(token).decode("utf-8"))

    def delete(
        self, k8scluster_id,
    ):
        """Delete a K8s Cluster.

        :param k8scluster_id: the cluster ID
        """
        print(get_client().k8s_cluster.delete(k8scluster_id=k8scluster_id))

    def wait_for_status(
        self, k8scluster_id, status=[], timeout_secs=60,
    ):
        """Wait for K8s Cluster to have one or more statuses.

        :param k8scluster_id: Cluster id with format: /api/v2/k8scluster/[0-9]+
        :param status: status(es) to wait for with format:
            ['status1', 'status2', 'statusn']
        :param timeout_secs: how many secs to wait before exiting
        :returns True/False if status was found within timeout_secs. May
            raise APIException.
        """
        cluster_status = [K8sClusterStatus[s] for s in status]

        try:
            success = get_client().k8s_cluster.wait_for_status(
                k8scluster_id=k8scluster_id,
                status=cluster_status,
                timeout_secs=timeout_secs,
            )
        except Exception:
            success = False

        if not success:
            print(
                "Failed to reach state(s) {} in {}".format(
                    str(status), str(timeout_secs),
                )
            )
            sys.exit(1)

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
        assert output in [
            "json",
            "text",
        ], "'output' parameter ust be 'json' or 'text'"

        assert major_filter is None or isinstance(
            major_filter, int
        ), "'major_filter' if provided must be an int"
        assert minor_filter is None or isinstance(
            minor_filter, int
        ), "'minor_filter' if provided must be an int"
        assert patch_filter is None or isinstance(
            patch_filter, int
        ), "'patch_filter' if provided must be an int"

        vers = []
        for v in get_client().k8s_cluster.k8s_supported_versions():
            if (
                (
                    major_filter is not None
                    and not v.startswith(str(major_filter))
                )
                or (
                    minor_filter is not None
                    and not v.find("." + str(minor_filter) + ".") > 0
                )
                or (
                    patch_filter is not None
                    and not v.endswith(str(patch_filter))
                )
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

    def get(
        self, output="yaml",
    ):
        """Get the system and user locks.

        :param output: how to display the output ['yaml'|'json']
        """
        response = get_client().lock.get()

        if output == "yaml":
            print(
                yaml.dump(
                    yaml.load(json.dumps(response), Loader=yaml.FullLoader,)
                )
            )
        else:
            print(response)

    def list(
        self, output="yaml",
    ):
        """List the system and user locks.

        :param output: how to display the output ['yaml'|'json']
        """
        self.get(output=output)

    def create(
        self, reason,
    ):
        """Create a lock."""
        get_client().lock.create(reason)
        print("Done")

    def delete(
        self, lock_id,
    ):
        """Delete a user lock."""
        print(get_client().lock.delete(lock_id))

    def delete_all(
        self, timeout_secs=300,
    ):
        """Delete all locks."""
        print(get_client().lock.delete_all(timeout_secs=300))


class LicenseProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.license>`."""

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
            print(response)
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

    def register(
        self, server_filename,
    ):
        """Register a license.

        :param server_filename: Filepath to the license on the server, e.g.
            '/srv/bluedata/license/LICENSE-1.txt'
        """
        get_client().license.register(server_filename=server_filename)
        print("Done.")

    def upload_with_ssh_key(
        self,
        server_filename,
        ssh_key_file=None,
        ssh_key_data=None,
        license_file=None,
        base64enc_license_data=None,
    ):
        """Not implemented yet.

        Workaround:
        -----------
         - scp your license to '/srv/bluedata/license/' on the controller
         - run client.license.register(server_filename) to register the license
        """
        raise Exception(
            "Not implemented yet! Workaround: scp your license to"
            "'/srv/bluedata/license/'"
        )

    def upload_with_ssh_pass(
        self,
        server_filename,
        ssh_username,
        ssh_password,
        license_file=None,
        base64enc_license_data=None,
    ):
        """Not implemented yet.

        Workaround:
        -----------
         - scp your license to '/srv/bluedata/license/' on the controller
         - run client.license.register(server_filename) to register the license
        """
        raise Exception(
            "Not implemented yet! Workaround: scp your license to"
            "'/srv/bluedata/license/'"
        )

    def delete(
        self, license_key,
    ):
        """Delete a license by LicenseKey.

        :param license_key: The license key, e.g. '1234 1234 ... 1234
            "SOMETEXT"'

        TIP: use `hpecp license list --license_key_only True` to get the
            license key
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
        print(response.text)

    def delete(
        self, url,
    ):
        """Make HTTP DELETE request.

        Examples
        --------
        $ hpecp httpclient delete /api/v1/workers/1
        """
        response = get_client()._request(
            url, http_method="delete", description="CLI HTTP DELETE",
        )
        print(response.text)

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
        print(response.text)

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
        print(response.text)


class UserProxy:
    """Proxy object to :py:attr:`<hpecp.client.user>`."""

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

    def list(
        self, output="table", columns=User.default_display_fields,
    ):
        """Retrieve the list of Users.

        :param output: how to display the output [text|table|json]
        """
        if output == "table":
            print(get_client().user.list().tabulate(columns=columns))
        elif output == "text":
            print(
                get_client()
                .user.list()
                .tabulate(
                    columns=columns, style="plain", display_headers=False,
                )
            )
        else:
            print(get_client().user.list().json)


class RoleProxy(object):
    """Proxy object to :py:attr:`<hpecp.client.role>`."""

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


class AutoComplete:
    """Shell autocompletion scripts.

    Example Usage:

    hpecp autocomplete bash > hpecp-bash.sh && source hpecp-bash.sh
    """

    def bash(self,):
        """Create autocompletion script for bash."""
        print(
            """_hpecp_complete()
{
    local cur prev BASE_LEVEL

    COMPREPLY=()
    cur=${COMP_WORDS[COMP_CWORD]}
    prev=${COMP_WORDS[COMP_CWORD-1]}

    COMP_WORDS_AS_STRING=$(IFS=, ; echo "${COMP_WORDS[*]}")

    case "$COMP_WORDS_AS_STRING" in

        ###############
        ### gateway ###
        ###############

        *"hpecp,gateway,create-with-ssh-key"*)
            COMPREPLY=( $(compgen \
                        -f -W "--ip --proxy-node-hostname --ssh-key --ssh-key-file --tags" \
                        -- $cur) )
            ;;
        *"hpecp,gateway"*)
            COMPREPLY=( $(compgen \
                        -W "create-with-ssh-key create-with-ssh-password delete get list states wait-for-delete wait-for-state" \
                        -- $cur) )
            ;;

        ###############
        ### k8sworker ###
        ###############

        *"hpecp,k8sworker,create-with-ssh-key"*)
            COMPREPLY=( $(compgen \
                        -f  -W "--ip --ssh-key --ssh-key-file --tags" \
                        -- $cur) )
            ;;
        *"hpecp,k8sworker"*)
            COMPREPLY=( $(compgen \
                        -W "create-with-ssh-key delete get list " \
                        -- $cur) )
            ;;


        ###############
        ### license ###
        ###############

        *"hpecp,license"*)
            COMPREPLY=( $(compgen \
                        -W "delete delete-all list platform-id register upload-with-ssh-key upload-with-ssh-pass" \
                        -- $cur) )
            ;;

        ####################
        ### autocomplete ###
        ####################

        *"hpecp,autocomplete,bash"*)
            COMPREPLY=( )
            ;;
        *"hpecp,autocomplete"*)
            COMPREPLY=( $(compgen \
                        -W "bash" \
                        -- $cur) )
            ;;
        *"hpecp"*)
            COMPREPLY=( $(compgen \
                      -W "autocomplete configure-cli gateway httpclient k8scluster k8sworker license lock" \
                      -- $cur) )
            ;;
    esac

    return 0

} &&
complete -F _hpecp_complete hpecp
        """  # noqa: E501
        )


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


class CLI(object):
    """Command Line Interface for the HPE Container Platform."""

    def __init__(self,):
        """Create a CLI instance."""
        self.catalog = CatalogProxy()
        self.k8sworker = K8sWorkerProxy()
        self.k8scluster = K8sClusterProxy()
        self.gateway = GatewayProxy()
        self.lock = LockProxy()
        self.license = LicenseProxy()
        self.httpclient = HttpClientProxy()
        self.user = UserProxy()
        self.role = RoleProxy()
        self.autocomplete = AutoComplete()
        self.configure_cli = configure_cli


if __name__ == "__main__":
    fire.Fire(CLI)
