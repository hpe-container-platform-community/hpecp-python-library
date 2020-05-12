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





