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

## Logging

Log level is controlled with the environment variable `LOG_LEVEL`.

You may set it programmatically in your code:

```py3
os.environ["LOG_LEVEL"] = "DEBUG"
```

Typical valid values are `ERROR`, `WARNING`, `INFO`, `DEBUG`. For a full list of values, see [here](https://docs.python.org/3/library/logging.html#logging-levels)

## Basic Usage

```py3
from hpecp import ContainerPlatformClient

client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session()

for tenant in client.epic_tenant.list():
    # shorten name and description fields if they are too long
    name = (tenant.name[0:18] + '..') if len(tenant.name) > 20 else tenant.name
    description = (tenant.description[0:38] + '..') if len(tenant.description) > 40 else tenant.description
    
    print( "{:>2} | {:>20} | {:>40} | {:>10}".format( tenant.tenant_id, name, description, tenant.status) )

# Configure HPE CP global authentication
active_directory_host = "10.1.0.77"
client.config.auth(
            { "external_identity_server":  {
                "bind_pwd":"5ambaPwd@",
                "user_attribute":"sAMAccountName",
                "bind_type":"search_bind",
                "bind_dn":"cn=Administrator,CN=Users,DC=samdom,DC=example,DC=com",
                "host":active_directory_host,
                "security_protocol":"ldaps",
                "base_dn":"CN=Users,DC=samdom,DC=example,DC=com",
                "verify_peer": False,
                "type":"Active Directory",
                "port":636 }
            })
```
