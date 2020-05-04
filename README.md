[![Build Status](https://travis-ci.org/hpe-container-platform-community/hpecp-python-library.svg?branch=master)](https://travis-ci.org/hpe-container-platform-community/hpecp-python-library)
[![Issues](https://img.shields.io/github/issues/hpe-container-platform-community/hpecp-python-library/bug.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/issues?q=is%3Aissue+is%3Aopen+label%3A"bug")
[![Coverage Status](https://coveralls.io/repos/github/hpe-container-platform-community/hpecp-python-library/badge.png?branch=master)](https://coveralls.io/github/hpe-container-platform-community/hpecp-python-library?branch=master)
[![Pyversions](https://img.shields.io/badge/Pyversions-2.7,%203.5,%203.6,%203.7,%203.8-green.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/tox.ini#L7)
[![Apache2 license](http://img.shields.io/badge/license-apache2-brightgreen.svg)](http://opensource.org/licenses/Apache-2.0)

----

```diff
- This project is a prototype - not much to see here yet!
- APIs are very likely to change between commits and could break your code.
```

## Installation

```shell
pip install --upgrade git+https://github.com/hpe-container-platform-community/hpecp-client@master
```

## Basic Usage

For development purpose, you can setup a tunnel to the controller allowing you to use `127.0.0.1` for the `api_host`:

```bash
./generated/ssh_controller.sh -L 8080:localhost:8080
```

Python commands:

```py3
from hpecp import ContainerPlatformClient

client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session() # Login

client.k8s_cluster.list().tabulate(columns=['description', 'id'])
```

Displays:
```
+-------------+-----------------------+
| description |          id           |
+-------------+-----------------------+
| my cluster  | /api/v2/k8scluster/20 |
+-------------+-----------------------+
```

## Examples

See [./docs/scripts](./docs/scripts) for more examples.

See [Notebook](https://nbviewer.jupyter.org/github/hpe-container-platform-community/hpecp-python-library/blob/master/docs/scripts/cluster_get_k8s_and_list_pods.ipynb) example creating a K8S cluster and listing pods.

## Logging

Log level is controlled with the environment variable `LOG_LEVEL`.

You may set it programmatically in your code:

```python
import os
os.environ["LOG_LEVEL"] = "DEBUG"
```

Typical valid values are `ERROR`, `WARNING`, `INFO`, `DEBUG`. For a full list of values, see [here](https://docs.python.org/3/library/logging.html#logging-levels)

- `INFO`: Significant Events
- `DEBUG`: API Request Parameters

## Documentation

https://hpe-container-platform-community.github.io/hpecp-python-library/index.html (coming soon)

## Features Implemented

| Group        | Method                  | Status   | Bugs/Features        |
| -------------|-------------------------| --------:|----------------------|
| Session      | [Create Session](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.client.html#hpecp.client.ContainerPlatformClient.create_session) (login)  | Complete | Reconnect on session expiration [#2](https://github.com/hpe-container-platform-community/hpecp-python-library/issues/2) |
| K8s Cluster  | Create                  | Complete |                      |
|              | List                    | Complete |                      |
|              | Get                     | Complete |                      |
|              | Delete                  | Complete |                      |
|              | Watch for status        | Complete |                      |
| Tenant       | ...                     |          |                      |
