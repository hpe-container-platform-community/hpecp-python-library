.. _apidocs:

API Docs
========

.. toctree::
   :maxdepth: 4

   hpecp.client
   hpecp.config
   hpecp.gateway
   hpecp.exceptions
   hpecp.k8s_cluster
   hpecp.k8s_worker
   hpecp.license
   hpecp.lock
   hpecp.logger
   hpecp.tag
   hpecp.tenant


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

