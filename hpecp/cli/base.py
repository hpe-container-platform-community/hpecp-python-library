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
import json
import os
import sys
import jmespath
import six
import yaml
import wrapt
import traceback

from hpecp.logger import Logger

from hpecp import (
    APIException,
    APIItemConflictException,
    ContainerPlatformClient,
    ContainerPlatformClientException,
)

from hpecp.exceptions import (
    APIForbiddenException,
    APIItemNotFoundException,
    APIUnknownException,
)
from hpecp.cli_utils import TextOutput

_log = Logger.get_logger()


def get_profile():
    """Retrieve the profile - if supplied."""
    profile = os.getenv("PROFILE", default="default")
    _log.debug(
        "PROFILE envirionment variable exists with value '{}'".format(profile)
    )
    return profile


def get_config_file():
    """Retrieve the CLI config file."""
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
    return HPECP_CONFIG_FILE


@wrapt.decorator
def intercept_exception(wrapped, instance, args, kwargs):
    """Handle Exceptions."""  # noqa: D202

    def _unknown_exception_handler(ex):
        """Handle unknown exceptions."""
        if _log.level == 10:  # "DEBUG"
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
        _log.debug(ex)
        sys.exit(1)

    try:
        return wrapped(*args, **kwargs)
    except SystemExit as se:
        sys.exit(se.code)
    except AssertionError as ae:
        print(ae, file=sys.stderr)
        sys.exit(1)
    except APIUnknownException as ue:
        _unknown_exception_handler(ue)
    except (
        APIException,
        APIItemNotFoundException,
        APIItemConflictException,
        APIForbiddenException,
        ContainerPlatformClientException,
    ) as e:
        print(e.message, file=sys.stderr)
        sys.exit(1)
    except Exception as ex:
        _unknown_exception_handler(ex)


@intercept_exception
def get_client(start_session=True):
    """Retrieve a reference to an authenticated client object."""
    client = ContainerPlatformClient.create_from_config_file(
        config_file=get_config_file(), profile=get_profile(),
    )
    if start_session:
        client.create_session()
    return client


@six.add_metaclass(abc.ABCMeta)
class BaseProxy:
    """Base 'proxy' class for generic calls to API."""

    def new_instance(self, client_module_name, resource_class):
        """Create a new instance (constructor).

        Parameters
        ----------
        client_module_name : str
            Name of the property in the ContainerPlatformClient that
            points to the different modules (user, gateway, cluster, etc)
        """
        self.client_module_name = client_module_name
        self.resource_class = resource_class
        super(BaseProxy, self).__init__()

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
        json_data = response.json

        if output == "json":
            print(json.dumps(json_data))
        elif output == "json-pp":
            print(json.dumps(json_data, indent=4, sort_keys=True,))
        else:

            print(
                yaml.dump(
                    yaml.load(json.dumps(json_data), Loader=yaml.FullLoader,)
                )
            )

    @intercept_exception
    def delete(self, id, wait_for_delete_sec=0):
        """Delete a resource.

        :param id: the resource ID
        :param wait_for_delete_sec: wait for delete to complete
        (0 = do not wait)
        """
        self.client = get_client()
        self.client_module_property = getattr(
            self.client, self.client_module_name
        )
        self.client_module_property.delete(id=id)

        if wait_for_delete_sec > 0:
            self.wait_for_delete(id=id, timeout_secs=wait_for_delete_sec)

    @intercept_exception
    def list(self, output="table", columns="DEFAULT", query={}):
        """Retrieve the list of resources.

        Parameters
        ----------
        output : str, optional
            Define how the output should be printed, by default "table"
            "json" or "json-pp" (json pretty print) if providing a query
        columns : list/tuple, optional
            List of specific columns to be displayed, by default []
            `Catalog.default_display_fields`
            "DEFAULT", "WIDE", or columns list
        query : dict, optional
            Query in jmespath (https://jmespath.org/) format, by default {}
            if using a query, output must be "json" or "json-pp"
        """
        if columns is not None:
            if columns == "DEFAULT":
                columns = list(self.resource_class.default_display_fields)
            elif columns == "WIDE":
                columns = list(self.resource_class.all_fields)
            elif isinstance(columns, tuple):
                columns = list(columns)
            elif isinstance(columns, str):
                columns = columns.split(",")

        # FIXME: this also gets called by print_list()
        self.validate_list_params(
            all_fields=self.resource_class.all_fields,
            output=output,
            columns=columns,
            query=query,
        )

        self.client = get_client()
        self.client_module_property = getattr(
            self.client, self.client_module_name
        )
        list_instance = self.client_module_property.list()

        self.print_list(
            list_instance=list_instance,
            output=output,
            columns=columns,
            query=query,
        )

    @intercept_exception
    def validate_list_params(self, all_fields, output, columns, query):
        """Print a list of resources.

        Parameters
        ----------
        list_instance : [type]
            [description]
        output : [type]
            [description]
        columns : [type]
            [description]
        query : [type]
            [description]
        """
        if not isinstance(columns, list):
            print("'columns' parameter must be a list.", file=sys.stderr)
            sys.exit(1)
        for col in columns:
            if col not in all_fields:
                print("Unknown column '{}'.".format(col), file=sys.stderr)
                sys.exit(1)

        if len(query) == 0:
            if output not in ["table", "text"]:
                print(
                    "When providing the --columns param, the --output param "
                    "must be 'table' or 'text'",
                    file=sys.stderr,
                )
                sys.exit(1)
        else:
            if output not in ["json", "json-pp", "text"]:
                print(
                    (
                        "If you provide a jmes --query, the output must "
                        "be 'json', 'json-pp', or 'text'"
                    ),
                    file=sys.stderr,
                )
                sys.exit(1)

    @intercept_exception
    def print_list(self, list_instance, output, columns, query):
        """Print a list of resources.

        Parameters
        ----------
        list_instance : [type]
            [description]
        output : [type]
            [description]
        columns : [type]
            [description]
        query : [type]
            [description]
        """
        if columns == "DEFAULT":
            columns = list_instance.resource_class.default_display_fields
        elif columns == "WIDE":
            columns = list_instance.resource_class.all_fields

        self.validate_list_params(
            all_fields=list_instance.resource_class.all_fields,
            output=output,
            columns=columns,
            query=query,
        )

        # use tabulate for simplified user output
        if len(query) == 0:
            if output == "table":
                print(list_instance.tabulate(columns=columns))
            else:
                print(
                    list_instance.tabulate(
                        columns=columns, style="plain", display_headers=False
                    )
                )

        # user has provided a jmes query
        else:
            data = list_instance.json
            if output == "json-pp":
                print(
                    json.dumps(
                        jmespath.search(str(query), data),
                        indent=4,
                        sort_keys=True,
                    )
                )
            elif output == "text":
                obj = jmespath.search(str(query), data)
                print(TextOutput.dump(obj))
            else:
                print(json.dumps(jmespath.search(str(query), data),))

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
