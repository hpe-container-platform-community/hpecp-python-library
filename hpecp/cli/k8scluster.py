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


import base64
import json
import six
import sys
import yaml

from textwrap import dedent

from hpecp.k8s_cluster import (
    K8sCluster,
    K8sClusterStatus,
    K8sClusterHostConfig,
)
from hpecp.cli import base


class K8sClusterProxy(base.BaseProxy):
    """Proxy object to :py:attr:`<hpecp.client.k8s_cluster>`."""

    def __dir__(self):
        """Return the CLI method names."""
        return [
            "add_addons",
            "admin_kube_config",
            "create",
            "dashboard_url",
            "dashboard_token",
            "delete",
            "examples",
            "get",
            "get_available_addons",
            "get_installed_addons",
            "import_cluster",
            "import_generic_cluster",
            "import_generic_cluster_with_json",
            "k8smanifest",
            "k8s_supported_versions",
            "list",
            "statuses",
            "upgrade_cluster",
            "wait_for_status",
        ]

    def __init__(self):
        """Create instance of proxy class with the client module name."""
        super(K8sClusterProxy, self).new_instance("k8s_cluster", K8sCluster)

    @base.intercept_exception
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
        addons=[],
        external_identity_server={},
        ext_id_svr_bind_pwd=None,
        ext_id_svr_user_attribute=None,
        ext_id_svr_bind_type=None,
        ext_id_svr_bind_dn=None,
        ext_id_svr_host=None,
        ext_id_svr_group_attribute=None,
        ext_id_svr_security_protocol=None,
        ext_id_svr_base_dn=None,
        ext_id_svr_verify_peer=None,
        ext_id_svr_type=None,
        ext_id_svr_port=None,
        external_groups=[],
        datafabric=False,
        datafabric_name=None,
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
        :param addons: list of required addons. See:
            `hpecp k8scluster get-available-addons`
        :param external_identity_server: dict (deprecated)
           Example '{"bind_pwd":"password",
                "user_attribute":"CN",
                "bind_type":"search_bind",
                "bind_dn":"cn=Administrator,CN=Users,DC=samdom,DC=example,DC=com",
                "host":"10.1.0.15",
                "group_attribute":"member",
                "security_protocol":"ldaps",
                "base_dn":"CN=Users,DC=samdom,DC=example,DC=com",
                "verify_peer":false,
                "type":"Active Directory",
                "port":636}'
        :param ext_id_svr_bind_pwd str
        :param ext_id_svr_user_attribute str
        :param ext_id_svr_bind_type str
        :param ext_id_svr_bind_dn str
        :param ext_id_svr_host str
        :param ext_id_svr_group_attribute str
        :param ext_id_svr_security_protocol str
        :param ext_id_svr_base_dn str
        :param ext_id_svr_verify_peer bool
        :param ext_id_svr_type str
        :param ext_id_svr_port int
        """
        host_config = [
            K8sClusterHostConfig.create_from_list(h.split(":"))
            for h in k8shosts_config.split(",")
        ]

        if external_identity_server:
            if not isinstance(external_identity_server, dict):
                print(
                    (
                        "Could not parse 'external_identity_server' parameter"
                        " - is it valid json?\n"
                        "Received: " + external_identity_server + "\n"
                    ),
                    file=sys.stderr,
                )
                sys.exit(1)
        else:
            external_identity_server = {}

        if ext_id_svr_bind_pwd is not None:
            external_identity_server["bind_pwd"] = ext_id_svr_bind_pwd

        if ext_id_svr_user_attribute is not None:
            external_identity_server[
                "user_attribute"
            ] = ext_id_svr_user_attribute

        if ext_id_svr_bind_type is not None:
            external_identity_server["bind_type"] = ext_id_svr_bind_type

        if ext_id_svr_bind_dn is not None:
            external_identity_server["bind_dn"] = ext_id_svr_bind_dn

        if ext_id_svr_host is not None:
            external_identity_server["host"] = ext_id_svr_host

        if ext_id_svr_group_attribute is not None:
            external_identity_server[
                "group_attribute"
            ] = ext_id_svr_group_attribute

        if ext_id_svr_security_protocol is not None:
            external_identity_server[
                "security_protocol"
            ] = ext_id_svr_security_protocol

        if ext_id_svr_base_dn is not None:
            external_identity_server["base_dn"] = ext_id_svr_base_dn

        if ext_id_svr_verify_peer is not None:
            external_identity_server["verify_peer"] = json.loads(
                ext_id_svr_verify_peer.lower()
            )

        if ext_id_svr_type is not None:
            external_identity_server["type"] = ext_id_svr_type

        if ext_id_svr_port is not None:
            external_identity_server["port"] = int(ext_id_svr_port)

        print(
            base.get_client().k8s_cluster.create(
                name=name,
                description=description,
                k8s_version=k8s_version,
                pod_network_range=pod_network_range,
                service_network_range=service_network_range,
                pod_dns_domain=pod_dns_domain,
                persistent_storage_local=persistent_storage_local,
                persistent_storage_nimble_csi=persistent_storage_nimble_csi,
                k8shosts_config=host_config,
                addons=addons,
                external_identity_server=external_identity_server,
                external_groups=external_groups,
                datafabric=datafabric,
                datafabric_name=datafabric_name,
            )
        )

    def admin_kube_config(self, id):
        """Retrieve a K8s Cluster Admin Kube Config.

        :param id: the cluster ID
        """
        print(
            base.get_client()
            .k8s_cluster.get(id)
            .admin_kube_config.replace(
                "\\n",
                "\n",
            )
        )

    def dashboard_url(
        self,
        id,
    ):
        """Retrieve a K8s Cluster Dashboard URL.

        :param id: the cluster ID
        """
        url = (
            base.get_client().k8s_cluster.get(id=id).dashboard_endpoint_access
        )
        print(url)

    def dashboard_token(
        self,
        id,
    ):
        """Retrieve a K8s Cluster Dashboard Token.

        :param id: the cluster ID
        """
        token = base.get_client().k8s_cluster.get(id=id).dashboard_token
        if six.PY2:
            print(base64.b64decode(token.encode()))
        else:
            print(base64.b64decode(token.encode()).decode("utf-8"))

    def examples(self):
        """Show examples for working with k8sclusters."""
        print(
            dedent(
                """\
                # retrieve id of k8s cluster with name 'c1'
                $ hpecp k8scluster list --query "[?label.name == 'c1'] | [0] | [_links.self.href]" --output text
                /api/v2/k8scluster/1
                """  # noqa:  E501
            )
        )

    @base.intercept_exception
    def k8smanifest(self):
        """Retrieve the k8smanifest."""
        response = base.get_client().k8s_cluster.k8smanifest()
        print(
            yaml.dump(
                yaml.load(
                    json.dumps(response),
                    Loader=yaml.FullLoader,
                )
            )
        )

    @base.intercept_exception
    def get_installed_addons(self, id):
        """Retrieve the installed addons on the cluster.

        :param id: get installed addons for a specific cluster
        """
        print(base.get_client().k8s_cluster.get(id=id).addons)

    @base.intercept_exception
    def get_available_addons(self, id=None, k8s_version=None):
        """Retrieve the available addons for a cluster.

        :param id: get available addons for a specific cluster (opt)
        :param k8s_version: get available addons for a cluster version (opt)
        """
        if id is not None and k8s_version is not None:
            print(
                "Either 'id' or 'k8s_version' parameter must be provided",
                file=sys.stderr,
            )
            sys.exit(1)

        if id is None and k8s_version is None:
            print(
                "Either 'id' or 'k8s_version' parameter must be provided",
                file=sys.stderr,
            )
            sys.exit(1)

        if id:
            print(base.get_client().k8s_cluster.get_available_addons(id=id))
        else:
            if not isinstance(k8s_version, str):
                print(
                    "'k8s_version' parameter must be quoted, e.g. \\\"1.20.11\\\" or \"'1.20.11'\"",
                    file=sys.stderr,
                    )
                sys.exit(1)
            print(
                base.get_client().k8s_cluster.get_available_addons(
                    k8s_version=k8s_version
                )
            )

    @base.intercept_exception
    def add_addons(self, id, addons, wait_for_ready_sec=0):
        """Retrieve the installed addons on the cluster.

        :param id: get installed addons for a specific cluster
        :param addons: list of addons to install
        :param wait_for_ready_sec: wait for ready status
        (0 = do not wait)
        """
        if id is None:
            print("'id' parameter must be provided.", file=sys.stderr)
            sys.exit(1)
        if addons is None or not isinstance(addons, list) or len(addons) < 1:
            print(
                "'addons' must be a list with at least one entry.",
                file=sys.stderr,
            )
            sys.exit(1)

        base.get_client().k8s_cluster.add_addons(id=id, addons=addons)

        if wait_for_ready_sec > 0:
            self.wait_for_status(
                id=id, status=["ready"], timeout_secs=wait_for_ready_sec
            )

    def statuses(
        self,
    ):
        """Return a list of valid statuses."""
        print([s.name for s in K8sClusterStatus])

    @base.intercept_exception
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
        for v in base.get_client().k8s_cluster.k8s_supported_versions():
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

    @base.intercept_exception
    def upgrade_cluster(
        self, id, k8s_upgrade_version, worker_upgrade_percent=20
    ):
        """Upgrade a cluster.

        TODO

        Returns
        -------
        TODO

        Raises
        ------
        APIException
        """
        base.get_client().k8s_cluster.upgrade_cluster(
            id, k8s_upgrade_version, worker_upgrade_percent
        )

    @base.intercept_exception
    def import_cluster(
        self,
        cluster_type,
        name,
        description,
        pod_dns_domain,
        server_url,
        ca,
        bearer_token,
    ):
        """Import a k8s cluster.

        TODO

        Returns
        -------
        TODO

        Raises
        ------
        APIException
        """
        print(
            base.get_client().k8s_cluster.import_cluster(
                cluster_type,
                name,
                description,
                pod_dns_domain,
                server_url,
                ca,
                bearer_token,
            )
        )

    @base.intercept_exception
    def import_generic_cluster(
        self, name, description, pod_dns_domain, server_url, ca, bearer_token
    ):
        """Import a generic cluster.

        TODO

        Returns
        -------
        TODO

        Raises
        ------
        APIException
        """
        print(
            base.get_client().k8s_cluster.import_generic_cluster(
                name, description, pod_dns_domain, server_url, ca, bearer_token
            )
        )

    @base.intercept_exception
    def import_generic_cluster_with_json(
        self, json_file_path=None, json_content=None
    ):
        """Import a generic cluster from json.

        TODO

        Returns
        -------
        TODO

        Raises
        ------
        APIException
        """
        assert (
            json_file_path is not None or json_content is not None
        ), "Either --json-file-path or --json-content must be provided"

        assert (
            json_file_path is None or json_content is None
        ), "Either --json-file-path or --json-content must be provided."

        if json_file_path:
            try:
                with open(json_file_path, "r") as f:
                    json_content = f.read()
            except OSError:
                print(
                    "Could not open/read json-file-path: {}".format(
                        json_file_path
                    ),
                    file=sys.stderr,
                )
                sys.exit(1)

        json_content = json.loads(json_content)

        print(
            base.get_client().k8s_cluster.import_generic_cluster_with_json(
                json_content
            )
        )
