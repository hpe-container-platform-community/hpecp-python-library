[![Build & Test](https://github.com/hpe-container-platform-community/hpecp-python-library/workflows/Build%20&%20Test/badge.svg?branch=master&event=push)](https://github.com/hpe-container-platform-community/hpecp-python-library/actions?query=workflow%3A%22Build+%26+Test%22+branch%3Amaster)
[![Code Checks](https://github.com/hpe-container-platform-community/hpecp-python-library/workflows/Code%20Checks/badge.svg?branch=master&event=push)](https://github.com/hpe-container-platform-community/hpecp-python-library/actions?query=workflow%3A%22Code+Checks%22+branch%3Amaster)
[![Issues](https://img.shields.io/github/issues/hpe-container-platform-community/hpecp-python-library/bug.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/issues?q=is%3Aissue+is%3Aopen+label%3A"bug")
[![Coverage Status](https://coveralls.io/repos/github/hpe-container-platform-community/hpecp-python-library/badge.png?branch=master)](https://coveralls.io/github/hpe-container-platform-community/hpecp-python-library?branch=master)
[![Pyversions](https://img.shields.io/badge/Pyversions-2.7,%203.5,%203.6,%203.7,%203.8,%203.9-green.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/tox.ini#L7)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/hpe-container-platform-community/hpecp-python-library)
[![Good first issues open](https://img.shields.io/github/issues/hpe-container-platform-community/hpecp-python-library/good%20first%20issue.svg?label=good%20first%20issue)](https://github.com/hpe-container-platform-community/hpecp-python-library/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)


----

```diff
- This project is under active development.
- Method APIs may change between commits.
- Not all HPE CP APIs have been implemented.
- Help Wanted - please consider contributing!
```

## Documentation

See [here](https://hpe-container-platform-community.github.io/hpecp-python-library/index.html) for User Documentation.

## Contributing

See:

- [Developing Guide](./DEVELOPING.md)
- [Contribution Guide](./CONTRIBUTING.md)

## Installation

```shell
# ensure you have an up-to-date pip
pip3 install -U pip

# install hpecp directly from git
pip3 install --upgrade git+https://github.com/hpe-container-platform-community/hpecp-client@master
```

If you are installing on Centos 7.7 with only Python 2.7 see [here](./docs/README-INSTALL-HPECP-HOSTS.md) for a workaround

## Basic Library Usage

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
warn_ssl = False
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

## CLI example 2

```sh
# Retrieve variables with host details:
# - CTRL_PUB_IP controller AWS host public IP
# - GATW_PRV_IP gateway AWS host private IP
# - GATW_PRV_DNS gateway AWS host private DNS
# - AD_PRV_IP Active Directory AWS host private IP
source ./scripts/variables.sh

pip3 install --quiet --upgrade git+https://github.com/hpe-container-platform-community/hpecp-client@master

# Save the configuration file for the hpecp cli
export HPECP_CONFIG_FILE="./generated/hpecp.conf"
cat >$HPECP_CONFIG_FILE<<EOF
[default]
api_host = ${CTRL_PUB_IP}
api_port = 8080
use_ssl = True
verify_ssl = False
warn_ssl = False
username = admin
password = admin123
EOF

echo "Checking for LICENSE locally"
# Register license so workers can be fully installed
if [[ ! -f generated/LICENSE ]]; then
    echo "ERROR: File './generated/LICENSE' not found - please add it - platform ID: $(hpecp license platform-id)"
    echo "       After adding the file, run this script again"
    exit 1
fi

echo "Uploading LICENSE to Controller"
scp -o StrictHostKeyChecking=no -i "./generated/controller.prv_key" ./generated/LICENSE centos@${CTRL_PUB_IP}:/srv/bluedata/license/LICENSE
hpecp license delete-all
hpecp license register /srv/bluedata/license/LICENSE
hpecp license list

echo "Deleting and creating lock"
hpecp lock delete-all
hpecp lock create "Install Gateway"

# Remove existing gateways
EXISTING_GATEWAY_IDS=$(hpecp gateway list --columns "['id']" --output text)
for GW in ${EXISTING_GATEWAY_IDS}; do
   hpecp gateway delete ${GW}
done
# Wait for the Gateway to cease existence
for GW in ${EXISTING_GATEWAY_IDS}; do
   hpecp gateway wait-for-state ${GW} --states "[]" --timeout-secs 1200
done

echo "Configuring the Gateway"
GATEWAY_ID=$(hpecp gateway create-with-ssh-key $GATW_PRV_IP $GATW_PRV_DNS --ssh-key-file generated/controller.prv_key)

echo "Waiting for gateway to have state 'installed'"
hpecp gateway wait-for-state ${GATEWAY_ID} --states "['installed']" --timeout-secs 1200
hpecp gateway list
hpecp lock delete-all

echo "Configuring AD authentication"
JSON_FILE=$(mktemp)
trap "{ rm -f $JSON_FILE; }" EXIT
cat >$JSON_FILE<<-EOF
{
    "external_identity_server":  {
        "bind_pwd":"5ambaPwd@",
        "user_attribute":"sAMAccountName",
        "bind_type":"search_bind",
        "bind_dn":"cn=Administrator,CN=Users,DC=samdom,DC=example,DC=com",
        "host":"${AD_PRV_IP}",
        "security_protocol":"ldaps",
        "base_dn":"CN=Users,DC=samdom,DC=example,DC=com",
        "verify_peer": false,
        "type":"Active Directory",
        "port":636
    }
}
EOF
hpecp httpclient post /api/v2/config/auth --json-file ${JSON_FILE}

echo "Adding K8s workers"
WRKR_IDS=()
for WRKR in ${WRKR_PRV_IPS[@]}; do
    echo "   worker $WRKR"
    WRKR_ID="$(hpecp k8sworker create-with-ssh-key --ip ${WRKR} --ssh-key-file ./generated/controller.prv_key)"
    echo "       id $WRKR_ID"
    WRKR_IDS+=($WRKR_ID)
done

echo "Waiting for K8s workers to have state 'storage_pending'"
for WRKR in ${WRKR_IDS[@]}; do
    echo "   worker $WRKR"
    hpecp k8sworker wait-for-status ${WRKR} --status  "['storage_pending']"
done

echo "Setting K8s worker storage"
for WRKR in ${WRKR_IDS[@]}; do
    echo "   worker $WRKR"
    hpecp k8sworker set-storage --k8sworker_id ${WRKR} --persistent-disks=/dev/nvme1n1 --ephemeral-disks=/dev/nvme2n1
done

echo "Waiting for K8s workers to have state 'ready'"
for WRKR in ${WRKR_IDS[@]}; do
    echo "   worker $WRKR"
    hpecp k8sworker wait-for-status ${WRKR} --status  "['ready']"
done

# get the k8s worker IDs
hpecp k8sworker list

# Example output:
# +-----------+--------+------------------------------------------+------------+---------------------------+
# | worker_id | status |                 hostname                 |   ipaddr   |           href            |
# +-----------+--------+------------------------------------------+------------+---------------------------+
# |    16     | ready  | ip-10-1-0-178.us-west-2.compute.internal | 10.1.0.178 | /api/v2/worker/k8shost/16 |
# |    17     | ready  | ip-10-1-0-93.us-west-2.compute.internal  | 10.1.0.93  | /api/v2/worker/k8shost/17 |
# +-----------+--------+------------------------------------------+------------+---------------------------+

# get the HPE CP supported k8s 1.17.x version number
KVERS=$(hpecp k8scluster k8s-supported-versions --output text --major-filter 1 --minor-filter 17)
echo $KVERS

# replace IDs defined below with the ones from `hpecp k8sworker list'
MASTER_ID="/api/v2/worker/k8shost/16"
WORKER_ID="/api/v2/worker/k8shost/17"
MASTER_IP="10.1.0.178"

# create a K8s Cluster
CLUS_ID=$(hpecp k8scluster create clus1 ${MASTER_ID}:master,${WORKER_ID}:worker --k8s-version $KVERS)
echo $CLUS_ID

# wait until cluster is ready
watch hpecp k8scluster list

# check connectivity to cluster
ping -c 5 $MASTER_IP

export KUBECONFIG=./clus_kfg
hpecp k8scluster admin-kube-config ${CLUS_ID} > ${KUBECONFIG}

# test kubectl:
kubectl get pods --all-namespaces
```


