CLI Docs
========

Setup
-----

Install the library:


.. code-block:: bash

   # ensure you have an up-to-date pip
   pip3 install -U pip

   pip3 install --upgrade git+https://github.com/hpe-container-platform-community/hpecp-client@master


Create a configuration file:

.. code-block:: bash

    cat > ~/.hpecp.conf <<EOF
    [default]
    api_host = 127.0.0.1
    api_port = 8080
    use_ssl = True
    verify_ssl = False
    warn_ssl = False
    username = admin
    password = admin123
    EOF

**NOTE:** you can specify a different config file location with the environment variables `HPECP_CONFIG_FILE`.

Test your connectivity:

.. code-block:: bash

    hpecp license platform-id

    >>> aa8716be-bc74-4ffa-b838-d92e6934d224

Logging Level
-------------

Log level is controlled with the environment variable `LOG_LEVEL`. 

Typical valid values are `ERROR`, `WARNING`, `INFO`, `DEBUG` - the default value is `INFO`.

- `INFO` = Significant Events
- `DEBUG` = API Requests


.. code-block:: bash

    export LOG_LEVEL=DEBUG
    hpecp license platform-id

    >>> 2020-05-12 12:58:00,251 - ContainerPlatformClient - DEBUG - ContainerPlatformClient() created with username['admin']
    >>> 2020-05-12 12:58:00,923 - ContainerPlatformClient - DEBUG - REQ: license/get_platform_id : get https://35.163.22.120:8080/api/v1/license
    >>> 2020-05-12 12:58:01,571 - ContainerPlatformClient - DEBUG - RES: license/get_platform_id : get https://35.163.22.120:8080/api/v1/license : 200 {"state": "unlicensed", "_links": {"self": {"href": "/api/v1/license"}}, "uuid": "aa8716be-bc74-4ffa-b838-d92e6934d224"}
    >>> aa8716be-bc74-4ffa-b838-d92e6934d224

See https://docs.python.org/3.7/howto/logging.html for much more info on logging.


CLI Help
--------

Run `hpecp` without any arguments to retrieve a list of command groups::

    hpecp

Returns::

    NAME
        hpecp

    SYNOPSIS
        hpecp GROUP

    GROUPS
        GROUP is one of the following:

        gateway
        ...

Similary to see a list of subcommands (e.g. for the gateway command)::

    hpecp gateway --help

Returns::

    NAME
        hpecp gateway

    SYNOPSIS
        hpecp gateway COMMAND

    COMMANDS
        COMMAND is one of the following:

        create_with_ssh_key
        Create a Gateway using SSH key authentication

        create_with_ssh_password
        Not yet implemented

        delete
        Retrieve a Gateway by Id

        get
        Retrieve a Gateway by Id
        ...

And to see a subcommand's (e.g. get) arguments::

    hpecp gateway get --help

Returns::

    NAME
        hpecp gateway get - Retrieve a Gateway by Id

    SYNOPSIS
        hpecp gateway get GATEWAY_ID <flags>

    DESCRIPTION
        Retrieve a Gateway by Id

    POSITIONAL ARGUMENTS
        GATEWAY_ID
            the id of the gateway with format: '/api/v1/workers/[0-9]+'

    FLAGS
        --output=OUTPUT
            how to display the output ['yaml'|'json']

Example
-------

.. image:: _static/cli_example.gif
  :alt: CLI Example

Autocompletion
--------------


(this is currently broken - awaiting: https://github.com/google/python-fire/issues/255)	

The CLI supports auto completion, for bash use:

.. code-block:: bash

    hpecp -- --completion bash > ~/.hpecp_completion	
    echo source ~/.hpecp_completion >> ~/.bash_profile	


For zsh, or fish, change the command from `bash` to `zsh` or `fish` in the first command and 
add the completion script to your shell init script, `~/.zshrc` or `~/.config/fish/config.fish`.










