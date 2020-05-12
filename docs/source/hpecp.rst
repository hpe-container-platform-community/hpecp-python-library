.. _apidocs:

API Docs
========

.. toctree::
   :maxdepth: 4
   :caption: Completed APIs

   hpecp.client
   hpecp.gateway
   hpecp.k8s_cluster

.. toctree::
   :maxdepth: 4
   :caption: Work-in-progress APIs

   hpecp.k8s_worker
   hpecp.license
   hpecp.lock
   hpecp.config
   hpecp.tag
   hpecp.tenant
   hpecp.exceptions


Logging
-------

You may set log level programmatically in your code:


.. code-block:: python

    import os
    os.environ["LOG_LEVEL"] = "DEBUG"


Log level is also controlled with the environment variable `LOG_LEVEL` - the default value is `INFO`.

- `INFO` = Significant Events
- `DEBUG` = API Requests

See https://docs.python.org/3.7/howto/logging.html for much more info on logging.

