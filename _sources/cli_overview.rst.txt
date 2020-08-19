CLI Docs
========

Setup
-----

Install the library:


.. code-block:: bash

   pip3 install --upgrade hpecp


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










