[![Build & Test](https://github.com/hpe-container-platform-community/hpecp-python-library/workflows/Build%20&%20Test/badge.svg?branch=master&event=push)](https://github.com/hpe-container-platform-community/hpecp-python-library/actions?query=workflow%3A%22Build+%26+Test%22+branch%3Amaster)
[![Code Checks](https://github.com/hpe-container-platform-community/hpecp-python-library/workflows/Code%20Checks/badge.svg?branch=master&event=push)](https://github.com/hpe-container-platform-community/hpecp-python-library/actions?query=workflow%3A%22Code+Checks%22+branch%3Amaster)
[![Issues](https://img.shields.io/github/issues/hpe-container-platform-community/hpecp-python-library/bug.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/issues?q=is%3Aissue+is%3Aopen+label%3A"bug")
[![Coverage Status](https://coveralls.io/repos/github/hpe-container-platform-community/hpecp-python-library/badge.png?branch=master)](https://coveralls.io/github/hpe-container-platform-community/hpecp-python-library?branch=master)
[![Pyversions](https://img.shields.io/badge/Pyversions-2.7,%203.5,%203.6,%203.7,%203.8,%203.9-green.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/tox.ini#L7)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pypi](https://img.shields.io/pypi/v/hpecp.svg)](https://pypi.org/project/hpecp)

[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/hpe-container-platform-community/hpecp-python-library)
[![Good first issues open](https://img.shields.io/github/issues/hpe-container-platform-community/hpecp-python-library/good%20first%20issue.svg?label=good%20first%20issue)](https://github.com/hpe-container-platform-community/hpecp-python-library/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)


----

## Documentation

See [here](https://hpe-container-platform-community.github.io/hpecp-python-library/index.html) for User Documentation.

## Contributing

See:

- [Developing Guide](https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/DEVELOPING.md)
- [Contribution Guide](https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/CONTRIBUTING.md)

## Installation

```shell
pip3 install -U hpecp
```

If you encounter an issue installing on Centos 7.7 with Python 2.7 see [here](https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/docs/README-INSTALL-HPECP-HOSTS.md) for a workaround


## CLI examples

You need to create a config file with your endpoint details - note that you can have multiple profiles:

```ini
cat > ~/.hpecp.conf <<EOF
[default]
api_host = 127.0.0.1
api_port = 8080
use_ssl = True
verify_ssl = False
warn_ssl = False
username = admin
password = admin123

[tenant1]
tenant = /api/v1/tenant/15
admin = ad_admin1
password = pass123
EOF
```

Setup bash autocomplete:
```sh
source <(hpecp autocomplete bash)
```

Autocompletion:
```sh
hpecp TAB
```

Add gateway:
```sh
hpecp lock create "Install Gateway"
hpecp gateway create-with-ssh-key --ip 10.1.0.5 --proxy-node-hostname my.gateway.local --ssh-key-file controller_private.key
hpecp gateway wait-for-state ${GATEWAY_ID} --states [installed] --timeout-secs 1200
hpecp lock delete-all
```

Add K8s worker host:
```sh
hpecp k8sworker create-with-ssh-key \
    --ip 10.1.0.10 \
    --ssh-key-file controller_private.key \
    --persistent-disks /dev/nvme1n1 \
    --ephemeral-disks /dev/nvme2n1 \
    --wait-for-operation-secs 600
```

K8s versions:
```sh
hpecp k8scluster k8s-supported-versions --major-filter 1 --minor-filter 17
```

Create k8s cluster:
```sh
hpecp k8scluster create --name myclus1 --k8shosts-config /api/v2/worker/k8shost/1:master --k8s_version=1.17.0
```

Get k8s available addons:
```sh
hpecp k8scluster get-available-addons --id $CLUSTER_ID
```

Add k8s cluster addons:
```sh
hpecp k8scluster add-addons --id $CLUSTER_ID --addons [istio,harbor]
```

List with columns parameter:
```sh
hpecp k8scluster list --columns [id,description,status]
```

List with (jmespath) query parameter:
```sh
hpecp catalog list --query "[?state!='installed' && state!='installing'] | [*].[_links.self.href] | []"  --output text
```

List --query examples:
```sh
hpecp tenant examples
```

Tenant create:
```sh
TENANT_ID=$(hpecp tenant create --name tenant1 --description "dev tenant" --k8s-cluster-id $CLUSTER_ID  --tenant-type k8s)
hpecp tenant wait-for-status --id $TENANT_ID --status [ready] --timeout-secs 600
```

Add LDAP role to Tenant:
```sh
ADMIN_GROUP="CN=DemoTenantAdmins,CN=Users,DC=samdom,DC=example,DC=com"
ADMIN_ROLE=$(hpecp role list  --query "[?label.name == 'Admin'][_links.self.href]" --output text)
hpecp tenant add-external-user-group --tenant-id $TENANT_ID --group $ADMIN_GROUP --role-id $ADMIN_ROLE
```

Add internal user to Tenant:

```sh
ADMIN_USER_ID=$(hpecp user list --query "[?label.name == 'admin'][_links.self.href]" --output text)
ADMIN_ROLE=$(hpecp role list  --query "[?label.name == 'Admin'][_links.self.href]" --output text)
hpecp tenant assign-user-to-role --tenant-id $TENANT_ID --role-id $ADMIN_ROLE --user-id $ADMIN_USER_ID
```

Tenant kube config:
```sh
PROFILE=tenant1 hpecp tenant k8skubeconfig > tenant1_kube.conf

# get available Kubedirector apps
kubectl --kubeconfig tenant1_kube.conf -n t1 get kubedirectorapps

# list running applications
kubectl --kubeconfig tenant1_kube.conf -n t1 describe kubedirectorclusters
```

Http call:
```sh
hpecp httpclient get /some/uri
```

Use a different config file:
```sh
HPECP_CONFIG_FILE=myclus.conf hpecp do-something
```

Logging with HTTP tracing:
```sh
export LOG_LEVEL=DEBUG
hpecp do-something
```

More sophisticated CLI examples [here](https://github.com/bluedata-community/bluedata-demo-env-aws-terraform/tree/master/bin/experimental) 


## Python Library Examples

See docs: https://hpe-container-platform-community.github.io/hpecp-python-library/index.html

Example:

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

print(client.k8s_cluster.list(columns=['description', 'id']))
```

On my environment, this displays:
```
+-------------+-----------------------+
| description |          id           |
+-------------+-----------------------+
| my cluster  | /api/v2/k8scluster/20 |
+-------------+-----------------------+
```

