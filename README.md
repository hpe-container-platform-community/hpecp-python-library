[![Build Status](https://travis-ci.org/hpe-container-platform-community/hpecp-python-library.svg?branch=master)](https://travis-ci.org/hpe-container-platform-community/hpecp-python-library)
[![Issues](https://img.shields.io/github/issues/hpe-container-platform-community/hpecp-python-library/bug.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/issues?q=is%3Aissue+is%3Aopen+label%3A"bug")
[![Coverage Status](https://coveralls.io/repos/github/hpe-container-platform-community/hpecp-python-library/badge.png?branch=master)](https://coveralls.io/github/hpe-container-platform-community/hpecp-python-library?branch=master)
[![Pyversions](https://img.shields.io/badge/Pyversions-2.7,%203.5,%203.6,%203.7,%203.8,%203.9-green.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/tox.ini#L7)
[![Apache2 license](http://img.shields.io/badge/license-apache2-brightgreen.svg)](http://opensource.org/licenses/Apache-2.0)

----

```diff
- This project is a prototype - not much to see here yet!
- APIs are very likely to change between commits and could break your code.
```

## Installation

```shell
# ensure you have an up-to-date pip
pip3 install -U pip

# install hpecp directly from git
pip3 install --upgrade git+https://github.com/hpe-container-platform-community/hpecp-client@master
```

## Basic Usage

Python example:

```py3
from hpecp import ContainerPlatformClient

client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')
client.create_session() # Login

# Alternatively:
# client = ContainerPlatformClient.create_from_config_file().create_session()

print(client.k8s_cluster.list().tabulate(columns=['description', 'id']))
```

On my environment, this displays:
```
+-------------+-----------------------+
| description |          id           |
+-------------+-----------------------+
| my cluster  | /api/v2/k8scluster/20 |
+-------------+-----------------------+
```

## Documentation

[See here](https://hpe-container-platform-community.github.io/hpecp-python-library/index.html)

## Features Implemented

| Group        | Method                  | Library Code Status   | Docs Status | CLI Status | Bugs/Features        |
| -------------|-------------------------| --------:| --------:| --------:|----------------------|
| Client       | [Create with parameters](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.client.html#hpecp.client.ContainerPlatformClient)  | Complete | Complete | N/A | |
|              | [Create from config file](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.client.html#hpecp.client.ContainerPlatformClient.create_from_config_file)  | Complete | Complete | Complete | |
|              | [Create from env](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.client.html#hpecp.client.ContainerPlatformClient.create_from_env)  | Complete | Complete | Not Started | |
| Session      | [Create Session](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.client.html#hpecp.client.ContainerPlatformClient.create_session) (login)  | Complete | Complete | Complete | Reconnect on session expiration [#2](https://github.com/hpe-container-platform-community/hpecp-python-library/issues/2) |
| Gateway      | [Create with SSH Key](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.gateway.html#hpecp.gateway.GatewayController.create_with_ssh_key) | Needs tests | Not Started | Started | |
|              | [Create with SSH Password](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.gateway.html#hpecp.gateway.GatewayController.create_with_ssh_password) | Not Started | Not Started| Not Started | |
|              | [List](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.gateway.html#hpecp.gateway.GatewayController.list) | Started | Not Started | Started | [see #4](https://github.com/hpe-container-platform-community/hpecp-python-library/issues/4) |
|              | [Get](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.gateway.html#hpecp.gateway.GatewayController.get) | Started | Not Started | Started | [see #4](https://github.com/hpe-container-platform-community/hpecp-python-library/issues/4) |
|              | [Delete](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.gateway.html#hpecp.gateway.GatewayController.delete) | Started | Started | Started | |
|              | [Wait for State](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.gateway.html#hpecp.gateway.GatewayController.wait_for_state) | Started | Not Started | Not Started | |
| K8s Cluster  | [Create](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.k8s_cluster.html#hpecp.k8s_cluster.K8sClusterController.create) | Complete | Complete | Started |                     |
|              | [List](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.k8s_cluster.html#hpecp.k8s_cluster.K8sClusterController.list)  | Complete | Complete | Started |                     |
|              | [Get](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.k8s_cluster.html#hpecp.k8s_cluster.K8sClusterController.get) | Complete | Complete | Started |                     |
|              | [Delete](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.k8s_cluster.html#hpecp.k8s_cluster.K8sClusterController.delete)  | Complete | Complete | Started |                     |
|              | [Wait for status](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.k8s_cluster.html#hpecp.k8s_cluster.K8sClusterController.wait_for_status) | Complete | Complete | Started |                     |
|              | [Supported K8s Versions](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.k8s_cluster.html#hpecp.k8s_cluster.K8sClusterController.supported_k8s_versions) | Not Started | Not Started | Not Started | See [#3](https://github.com/hpe-container-platform-community/hpecp-python-library/issues/3) |
| License       | [Get Platform ID](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.license.html#hpecp.license.LicenseController.get_platform_id) | Started | Not Started| Not Started| |
|               | [Register](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.license.html#hpecp.license.LicenseController.register_license) | Started | Not Started| Not Started| |
|               | [List](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.license.html#hpecp.license.LicenseController.list)  | Started | Not Started| Not Started| |
|               | [Upload](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.license.html#hpecp.license.LicenseController.upload_license)  | Not Started | Not Started| Not Started| |
|               | [Delete](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.license.html#hpecp.license.LicenseController.delete_license) | Started | Not Started| Not Started| |
| Tenant       | ...                     |          |                      | | |


## Examples

See [./docs/scripts](./docs/scripts) for more examples.

See [Notebook](https://nbviewer.jupyter.org/github/hpe-container-platform-community/hpecp-python-library/blob/master/docs/scripts/cluster_get_k8s_and_list_pods.ipynb) example creating a K8S cluster and listing pods.

## CLI

CLI is installed with pip ([as above](#installation))

First you need to create a config file with your endpoint details.  

Note that you can have multiple profiles:

```ini
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
```

Create k8s cluster example:
```sh
hpecp k8scluster create myclus1 /api/v2/worker/k8shost/1:master --k8s_version=1.17.0
```

List k8s clusters example:
```sh
hpecp k8scluster tabulate --columns=['id','description','status']
```

#### Auto completion

(this is currently broken - awaiting: https://github.com/google/python-fire/issues/255)

The CLI supports auto completion, for bash use:

```sh
hpecp -- --completion bash > ~/.hpecp_completion
echo source ~/.hpecp_completion >> ~/.bashrc
```

For zsh, or fish, change the command type in the first command and add to the relevant startup script.

#### Source code

Source code for CLI: [./bin/hpecp](./bin/hpecp).

## Contributors

See [Developing README](./DEVELOPING.md)
