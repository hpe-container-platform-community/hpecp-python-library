Logging
=======

Logging level
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


Logging Configuration
---------------------

To change logging configuration, e.g. to log to a file, set the environment variable `HPECP_LOG_CONFIG_FILE` and provide a configuration file.

Example: `HPECP_LOG_CONFIG_FILE=~/.hpecp_logging.conf`:

.. code-block:: bash

    [loggers]
    keys=root,HPECP_CLI

    [handlers]
    keys=consoleHandler,fileHandler

    [formatters]
    keys=consoleFormatter,fileFormatter

    [logger_root]
    level=INFO
    handlers=consoleHandler,fileHandler

    [logger_HPECP_CLI]
    level=DEBUG
    handlers=fileHandler
    qualname=HPECP_CLI
    propagate=0

    [handler_consoleHandler]
    level=INFO
    class=StreamHandler
    formatter=consoleFormatter
    args=(os.devnull,)

    [handler_fileHandler]
    level=DEBUG
    class=FileHandler
    formatter=fileFormatter
    args=("/MY/LOG/FILE/LOCATION/hpecp.log","a")

    [formatter_consoleFormatter]
    format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
    datefmt=

    [formatter_fileFormatter]
    format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
    datefmt=

See https://docs.python.org/3.7/howto/logging.html for much more info on logging.


