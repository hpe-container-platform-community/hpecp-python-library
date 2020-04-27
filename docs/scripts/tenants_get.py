#!/usr/bin/env python3

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