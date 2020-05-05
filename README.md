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

print(client.k8s_cluster.list().tabulate(columns=['description', 'id']))
```

Displays:
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

| Group        | Method                  | Code Status   | Docs Status | Bugs/Features        |
| -------------|-------------------------| --------:| --------:|----------------------|
| Session      | [Create Session](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.client.html#hpecp.client.ContainerPlatformClient.create_session) (login)  | Complete | Complete | Reconnect on session expiration [#2](https://github.com/hpe-container-platform-community/hpecp-python-library/issues/2) |
| K8s Cluster  | [Create](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.k8s_cluster.html#hpecp.k8s_cluster.K8sClusterController.create) | Complete | Not Started |                     |
|              | [List](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.k8s_cluster.html#hpecp.k8s_cluster.K8sClusterController.list)  | Complete | Not Started |                     |
|              | [Get](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.k8s_cluster.html#hpecp.k8s_cluster.K8sClusterController.get) | Complete | Not Started |                     |
|              | [Delete](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.k8s_cluster.html#hpecp.k8s_cluster.K8sClusterController.delete)  | Complete | Not Started |                     |
|              | [Wait for status](https://hpe-container-platform-community.github.io/hpecp-python-library/hpecp.k8s_cluster.html#hpecp.k8s_cluster.K8sClusterController.wait_for_status) | Complete | Not Started |                     |
| Tenant       | ...                     |          |                      | |


## Examples

See [./docs/scripts](./docs/scripts) for more examples.

See [Notebook](https://nbviewer.jupyter.org/github/hpe-container-platform-community/hpecp-python-library/blob/master/docs/scripts/cluster_get_k8s_and_list_pods.ipynb) example creating a K8S cluster and listing pods.

## CLI

See CLI prototype in [./bin/](./bin/)

```
cat > ~/.hpecp.conf <<EOF
[default]
api_host = 127.0.0.1
api_port = 8080
use_ssl = True
verify_ssl = False

[demosrv]
username = admin
password = admin123
EOF
```

Create k8s cluster example:
```
hpecp k8s_cluster create myclus1 /api/v2/worker/k8shost/1:master --k8s_version=1.17.0 --profile=demosrv
```

List k8s clusters example:
```
hpecp k8s_cluster tabulate --columns=['id','description','status'] --profile=demosrv
```
