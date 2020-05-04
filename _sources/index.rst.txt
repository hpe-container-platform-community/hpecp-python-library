Overview
=========

Python library for HPE Container Platform (HPECP).

This library is pre-alpha. The API of this library may be unstable and 
subject to change until this library reaches beta.


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
   logging
   github
   license

