#!/usr/bin/env python3

from hpecp import ContainerPlatformClient
import time

client = ContainerPlatformClient(username='admin', 
                                password='admin123', 
                                api_host='127.0.0.1', 
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')

client.create_session()

try:
    print( client.license.register_license("/srv/bluedata/license/LICENSE") )
    time.sleep(5)
except:
    pass # Ignore errors if license already registered

license = client.license.get_license()
print( license )

print( client.license.delete_license( license['Licenses'][0]['LicenseKey']) )
time.sleep(5)

license = client.license.get_license()
print( license )
