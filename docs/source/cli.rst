.. _clidocs:

CLI Docs
========

Setup
-----

Install the library:


.. code-block:: bash

   pip3 install --upgrade git+https://github.com/hpe-container-platform-community/hpecp-client@master


Create a configuration file:

.. code-block:: bash

    cat > ~/.hpecp.conf <<EOF
    [default]
    api_host = 127.0.0.1
    api_port = 8080
    use_ssl = True
    verify_ssl = False
    ssl_warn = False
    username = admin
    password = admin123
    EOF

Test your connectivity:

.. code-block:: bash

    hpecp license platform-id
    >>> returns-your-unique-platform-id

Logging Level
-------------

Log level is controlled with the environment variable LOG_LEVEL.

Typical valid values are ERROR, WARNING, INFO, DEBUG. Default is DEBUG.

.. code-block:: bash

    export LOG_LEVEL=DEBUG
    hpecp license platform-id
    >>> returns-your-unique-platform-id



