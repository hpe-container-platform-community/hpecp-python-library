Overview
=========

Python library and Command Line Interface (CLI) for HPE Container Platform (HPECP).

This library is pre-alpha. The API of this library may be unstable and 
subject to change until this library reaches beta.

Library Example
---------------

Example basic usage with variables passed to client constructor:

First :ref:`install <Installation>` the library - then from your python environment ...

.. code-block:: python

   from hpecp import ContainerPlatformClient

   client = ContainerPlatformClient(username='admin', 
                                 password='admin123', 
                                 api_host='127.0.0.1', 
                                 api_port=8080,
                                 use_ssl=True,
                                 verify_ssl='/certs/hpecp-ca-cert.pem')

   client.create_session() # Login

   client.k8s_cluster.list().tabulate(columns=['description', 'id'])

Example basic usage with config file:

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

.. code-block:: python

   from hpecp import ContainerPlatformClient

   client = ContainerPlatformClient.create_from_config_file().create_session()

   client.k8s_cluster.list().tabulate(columns=['description', 'id'])

CLI Example
-----------

First create a configuration file.

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

Now :ref:`install <Installation>` the CLI.  After installing, the CLI will be available as `hpecp`:

.. code-block:: bash

    hpecp license platform-id

    >>> aa8716be-bc74-4ffa-b838-d92e6934d224

To find out what capabilities are available, enter:

.. code-block:: bash

    hpecp help

Contents
========

.. toctree::
   :maxdepth: 0

   installation
   hpecp
   cli_overview
   logging
   github
   license


