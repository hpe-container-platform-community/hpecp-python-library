[![Build Status](https://travis-ci.org/hpe-container-platform-community/hpecp-python-library.svg?branch=master)](https://travis-ci.org/hpe-container-platform-community/hpecp-python-library)
[![Issues](https://img.shields.io/github/issues/hpe-container-platform-community/hpecp-python-library/bug.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/issues?q=is%3Aissue+is%3Aopen+label%3A"bug")
[![Coverage Status](https://coveralls.io/repos/github/hpe-container-platform-community/hpecp-python-library/badge.png?branch=master)](https://coveralls.io/github/hpe-container-platform-community/hpecp-python-library?branch=master)
[![Pyversions](https://img.shields.io/badge/Pyversions-2.7,%203.5,%203.6,%203.7-green.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/tox.ini#L7)
[![Apache2 license](http://img.shields.io/badge/license-apache2-brightgreen.svg)](http://opensource.org/licenses/Apache-2.0)

----

```diff
- This project is a prototype - not much to see here yet!
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

# Print the list of Tenants
for tenant in client.epic_tenant.list():    
    print( "{:>2} | {:>10} | {}".format( tenant.tenant_id, tenant.status, tenant.name ) )
```

## Examples

See [./docs/scripts](./docs/scripts) for more examples.
