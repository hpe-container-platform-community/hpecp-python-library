#!/usr/bin/env python3

from hpecp import ContainerPlatformClient

client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session()

active_directory_host = None  # Set to  your AD IP Address

if active_directory_host is None:
    raise Exception("Aborting. You must set the variable 'active_directory_host'.")

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