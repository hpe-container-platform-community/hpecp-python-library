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

import collections
import configparser
import inspect
import os
import sys
from collections import OrderedDict
from textwrap import dedent

import fire
import six
from jinja2 import Environment

import hpecp
from hpecp import ContainerPlatformClient
from hpecp.cli.catalog import CatalogProxy
from hpecp.cli.datatap import DatatapProxy
from hpecp.cli.gateway import GatewayProxy
from hpecp.cli.httpclient import HttpClientProxy
from hpecp.cli.k8scluster import K8sClusterProxy
from hpecp.cli.k8sworker import K8sWorkerProxy
from hpecp.cli.license import LicenseProxy
from hpecp.cli.lock import LockProxy
from hpecp.cli.role import RoleProxy
from hpecp.cli.tenant import TenantProxy
from hpecp.cli.user import UserProxy


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

        modules = collections.OrderedDict()
        columns = collections.OrderedDict()

        for module_name in self.cli.__dict__.keys():

            # we manually define autocomplete for these methods
            if module_name in ["autocomplete", "configure_cli", "version"]:
                continue

            module = getattr(self.cli, module_name)
            function_names = dir(module)

            try:
                all_fields = getattr(module.resource_class, "all_fields")
            except Exception:
                all_fields = []

            function_parameters = collections.OrderedDict()

            # autcomplete should have most specific name first, e.g.
            # hpecp.tenant.create_xyz  before
            # hpecp.tenant.create
            for function_name in reversed(function_names):
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

            # _log = Logger.get_logger()
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

                MODULE=${COMP_WORDS[1]}

                COMP_WORDS_AS_STRING=$(IFS=. ; echo "${COMP_WORDS[*]}")

                # if last input was > for redirecting to a file
                # perform file and directory autocompletion
                if echo "${prev}" | grep -q '>'
                then
                    _filedir;
                    return
                fi



                declare -A MODULE_COLUMNS=(
                    {% for module_name in modules %}
                        {% set column_names = " ".join(columns[module_name]) %}
                        ['{{module_name}}']="{{column_names}}"
                    {% endfor %}
                )

                {% raw %}
                # list has uniform behaviour as it is implemented in base.BaseProxy
                if [[ "${COMP_WORDS[2]}" == "list" ]];
                then

                    # if 'list' was the last word
                    if [[ "${prev}" == "list" ]];
                    then
                        COMPREPLY=( $(compgen -W "--columns --query" -- $cur) )
                        return
                    fi



                    # '--columns' was the last word and user is entering column names
                    if [[ "${COMP_WORDS[3]}" == "--columns"* && ${#COMP_WORDS[@]} -le 5 ]];
                    then
                        declare -a COLUMNS=(${MODULE_COLUMNS[$MODULE]})

                        local realcur prefix
                        realcur=${cur##*,} # everything after the last comma, e.g. a,b,c,d -> d
                        prefix=${cur%,*}   # everything before the lat comma, e.g. a,b,c,d -> a,b,c

                        if [[ "$cur" == *,* ]];
                        then
                            IFS=',' ENTERED_COLUMNS_LIST=($prefix)
                            unset IFS
                        else
                            IFS=',' ENTERED_COLUMNS_LIST=($prev)
                            unset IFS
                        fi

                        for COLUMN in ${COLUMNS[@]}; do
                            for ENTERED_COLUMN in ${ENTERED_COLUMNS_LIST[@]}; do
                                if [[ "${ENTERED_COLUMN}" == "${COLUMN}" ]]
                                then
                                    # remove columns already entered by user
                                    COLUMNS=(${COLUMNS[*]//$ENTERED_COLUMN/})
                                fi
                            done
                        done

                        if [[ "$cur" == *,* ]];
                        then
                            COMPREPLY=( $(compgen -W "${COLUMNS[*]}" -P "${prefix}," -S "," -- ${realcur}) )
                            compopt -o nospace
                            return
                        else
                            COMPREPLY=( $(compgen -W "${COLUMNS[*]}" -S "," -- ${realcur}) )
                            compopt -o nospace
                            return
                        fi
                    fi

                    # user has finished entering column list or query
                    if [[ ${#COMP_WORDS[@]} == 6 ]];
                    then
                        COMPREPLY=( $(compgen -W "--output" -- $cur) )
                        return
                    fi

                    if [[ "${COMP_WORDS[5]}" == "--output"*  ]];
                    then
                        if [[ "${COMP_WORDS[3]}" == "--columns"*  ]];
                        then
                            COMPREPLY=( $(compgen -W "table text" -- $cur) )
                            return
                        else
                            COMPREPLY=( $(compgen -W "json json-pp text" -- $cur) )
                            return
                        fi
                    fi

                    return
                fi
                {% endraw %}

                # if the last parameter was --*file perform
                # file and directory autocompletion
                if echo "${prev}" | grep -q '\-\-.*file$'
                then
                    _filedir;
                    return
                fi

                # if last input was > for redirecting to a file
                # perform file and directory autocompletion
                if echo "${prev}" | grep -q '>'
                then
                    _filedir;
                    return
                fi

                case "$COMP_WORDS_AS_STRING" in

                {% set module_names = " ".join(modules.keys()) %}
                {% for module_name in modules %}
                    {% set function_names = " ".join(modules[module_name].keys()).replace('_', '-') %}
                    {% for function_name in modules[module_name] %}
                        {% set param_names = " ".join(modules[module_name][function_name]).replace('_', '-') %}
                        {% if function_name == "list" %}
                            # do nothing - already handled above
                        {% else %}
                    *"hpecp.{{module_name}}.{{function_name.replace('_', '-')}}."*)
                        PARAM_NAMES="{{param_names}}"
                        for PARAM in ${PARAM_NAMES[@]}; do
                            PARAM="${PARAM//'\'}"
                            for WORD in ${COMP_WORDS[@]}; do
                                if [[ "${WORD}" == "${PARAM}" ]]
                                then
                                    # remove parameters already entered by user
                                    PARAM_NAMES=${PARAM_NAMES//$WORD/}
                                fi
                            done
                        done
                        COMPREPLY=( $(compgen -W "$PARAM_NAMES" -- $cur) )
                        ;;
                        {% endif %}
                    {% endfor %}
                    *"hpecp.{{module_name}}"*)
                        COMPREPLY=( $(compgen -W "{{function_names}}" -- $cur) )
                        ;;
                {% endfor %}
                    *"hpecp.autocomplete.bash"*)
                        COMPREPLY=( )
                        ;;
                    *"hpecp.autocomplete"*)
                        COMPREPLY=( $(compgen -W "bash" -- $cur) )
                        ;;
                    *"hpecp"*)
                        COMPREPLY=( $(compgen -W "autocomplete configure-cli version {{module_names}}" -- $cur) )
                        ;;
                esac
                return 0
            } &&
            complete -F _hpecp_complete hpecp
        """  # noqa: E501,W605
        )

        (modules, columns) = self._get_metadata()

        print(
            Environment(trim_blocks=True, lstrip_blocks=True)
            .from_string(__bash_template)
            .render(modules=modules, columns=columns),
            file=sys.stdout,
        )


def version():
    """Display version information."""
    print("HPECP Version:  " + ContainerPlatformClient.version())
    print("HPECP Path:     " + hpecp.__file__)
    print("Python Version: " + sys.version.replace("\n", ""))
    print("Python Path:    " + sys.executable)


class CLI(object):
    """Command Line Interface for the HPE Container Platform."""

    def __dir__(self):
        """Return modules names."""
        return list(vars(self))

    def __init__(self,):
        """Create a CLI instance."""
        self.autocomplete = AutoComplete(self)
        self.configure_cli = configure_cli
        self.catalog = CatalogProxy()
        self.k8sworker = K8sWorkerProxy()
        self.k8scluster = K8sClusterProxy()
        self.tenant = TenantProxy()
        self.gateway = GatewayProxy()
        self.lock = LockProxy()
        self.license = LicenseProxy()
        self.httpclient = HttpClientProxy()
        self.user = UserProxy()
        self.role = RoleProxy()
        self.version = version
        self.datatap = DatatapProxy()


if __name__ == "__main__":
    fire.Fire(CLI)
