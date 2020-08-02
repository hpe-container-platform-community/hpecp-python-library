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

import sys
from hpecp.k8s_worker import WorkerK8sStatus, WorkerK8s
from hpecp.cli import base


class K8sWorkerProxy(base.BaseProxy):
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
        """Create instance of proxy class with the client module name."""
        super(K8sWorkerProxy, self).new_instance("k8s_worker", WorkerK8s)

    @base.intercept_exception
    def create_with_ssh_key(
        self,
        ip=None,
        ssh_key=None,
        ssh_key_file=None,
        tags=[],
        ephemeral_disks=None,
        persistent_disks=None,
        wait_for_operation_secs=0,
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
        ephemeral_disks : str
            Comma separated string containing ephemeral disks.
            e.g: "/dev/nvme2n1,/dev/nvme2n2"
        persistent_disks : str, optional
            Comma separated string containing persistent disks, by default
            None.
            e.g: "/dev/nvme1n1,/dev/nvme1n2"
        wait_for_operation_secs: int
            wait for operations to complete. 0 = don't wait
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
            try:
                with open(ssh_key_file) as f:
                    ssh_key = f.read()
            except OSError:
                print(
                    "Could not open/read ssh-key-file: {}".format(
                        ssh_key_file
                    ),
                    file=sys.stderr,
                )
                sys.exit(1)

        if (
            ephemeral_disks is not None or persistent_disks is not None
        ) and wait_for_operation_secs == 0:
            print(
                (
                    "If setting disks, 'wait-for-operation-secs' parameter"
                    " must be greater than zero (recommended 600 seconds)"
                ),
                file=sys.stderr,
            )
            sys.exit(1)

        worker_id = base.get_client().k8s_worker.create_with_ssh_key(
            ip=ip, ssh_key_data=ssh_key, tags=tags,
        )

        if wait_for_operation_secs > 0:
            self.wait_for_status(
                id=worker_id,
                status=["storage_pending", "error"],
                timeout_secs=wait_for_operation_secs,
            )

        if base.get_client().k8s_worker.get(id=worker_id).status == "error":
            print(
                (
                    "Create request has errored. "
                    "Check status message with `hpecp k8sworker get {}".format(
                        id
                    )
                ),
                file=sys.stderr,
            )
            sys.exit(1)

        if ephemeral_disks is not None or persistent_disks is not None:
            self.set_storage(
                id=worker_id,
                ephemeral_disks=ephemeral_disks,
                persistent_disks=persistent_disks,
            )

        if wait_for_operation_secs > 0:
            self.wait_for_status(
                id=worker_id,
                status=["ready"],
                timeout_secs=wait_for_operation_secs,
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

    @base.intercept_exception
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

        base.get_client().k8s_worker.set_storage(
            worker_id=id, persistent_disks=p_disks, ephemeral_disks=e_disks,
        )

    def statuses(self,):
        """Return a list of valid statuses."""
        print([s.name for s in WorkerK8sStatus])
