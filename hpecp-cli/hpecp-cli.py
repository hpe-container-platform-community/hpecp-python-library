import fire
from hpecp import ContainerPlatformClient

def k8s_cluster_list():
    """Example config:

    [default]
    api_host = 127.0.0.1
    api_port = 8080
    use_ssl = True
    verify_ssl = False

    [demosrv]
    username = admin
    password = admin123
    """
    client = ContainerPlatformClient.create_from_config_file(profile='demosrv')
    client.create_session()

    print(client.k8s_cluster.list().tabulate(columns=['id','description']))


if __name__ == '__main__':
  fire.Fire()