#!/usr/bin/env python3

from hpecp import ContainerPlatformClient

client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session()

###################################
# Configure Tenant authentication #
###################################

# Set up only the AD Admins Group
client.epic_tenant.auth_setup(
        tenant_id = 2,
        data =  {"external_user_groups":[{ 
            "role":"/api/v1/role/2", # 2 = Admins
            "group":"CN=DemoTenantAdmins,CN=Users,DC=samdom,DC=example,DC=com"
            }]}
    )

# Set up both the AD Admins and Members
client.epic_tenant.auth_setup(
        tenant_id = 2,
        data =  {"external_user_groups":[
            {
                "role":"/api/v1/role/2", # 2 = Admins
                "group":"CN=DemoTenantAdmins,CN=Users,DC=samdom,DC=example,DC=com"
            },
            { 
                "role":"/api/v1/role/3", # 3 = Members
                "group":"CN=DemoTenantUsers,CN=Users,DC=samdom,DC=example,DC=com"
            }]}
    )