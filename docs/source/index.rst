============
HPECP Python
============

Overview
=========

Python library for HPE Container Platform (HPECP).

Example usage:

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


Contents
========

.. toctree::
   :maxdepth: 1

   installation
   hpecp
   license

GitHub
======

   `hpecp-python-library repository <https://github.com/hpe-container-platform-community/hpecp-python-library>`_