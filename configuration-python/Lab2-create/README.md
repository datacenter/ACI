Lab2
====================

For beginner user, you can simply run the code directly:
eg: python createTenant.py
Then you just need to follow the Wizard to finish the configuration.

====================

For advanced user, you could put all the key arguments and optional arguments when you call the python code.
The format of the key arguments and optional argument for all the codes are list as below:


addSecurityDomain.py: to add security domains: such as "all" and "mgmt" to a tenant.
usage:
python addSecurityDomain.py <hostname> <username> <password> <tenant_name> <security_domain>
python addSecurityDomain.py 172.22.233.207 admin Cisco123 ACILab all

--------------------------------------------------------------------

buildBridgeDomainSubnet.py: to build a bridge domain and its associated a subnet. The bridge domain should connect to a private network (which is build by running buildPrivateL3Network). 
usage:
python buildBridgeDomainSubnet.py <hostname> <username> <password> <tenant_name> <bridge_domain> <subnet_ip> <network_name>
python buildBridgeDomainSubnet.py 172.22.233.207 admin Cisco123 ACILab ACILab_BD1 10.10.10.1/24 ACILab_VRF

--------------------------------------------------------------------

buildPrivateL3Network.py: to build a private level 3 network (context). It shall contain one bridge domain.
usage:
python buildPrivateL3Network.py <hostname> <username> <password> <tenant_name> <network_name>
python buildPrivateL3Network.py 172.22.233.207 admin Cisco123 ACILab ACILab_VRF

--------------------------------------------------------------------

createTenant.py: to create a tenant.
usage:
python createTenant.py <hostname> <username> <password> <tenant_name>
python createTenant.py 172.22.233.207 admin Cisco123 ACILab

--------------------------------------------------------------------

deleteBridgeDomain.py: to delete a bridge domain.
usage:
python deleteBridgeDomain.py <hostname> <username> <password> <tenant_name> <bridge_domain>
python deleteBridgeDomain.py 172.22.233.207 admin Cisco123 ACILab ACILab_BD1

--------------------------------------------------------------------

deletePrivateL3Network.py: to delete a private level 3 network.
usage:
python deletePrivateL3Network.py <hostname> <username> <password> <tenant_name> <network_name>
python deletePrivateL3Network.py 172.22.233.207 admin Cisco123 ACILab ACILab_VRF

--------------------------------------------------------------------

deleteTenant.py: to delete a tenant.
usage:
python deleteTenant.py <hostname> <username> <password> <tenant_name>
python deleteTenant.py 172.22.233.207 admin Cisco123 ACILab

--------------------------------------------------------------------

createTenantLab2.py:  a implement code that utilize all the codes under this folder in order to accomplish the tasks in Lab2 in Lab Guide (version 1.19)
usage:
python CreateTenantLab2.py <hostname> <username> <password> <tenant_name>
python CreateTenantLab2.py 172.22.233.207 admin Cisco123 ACILab

--------------------------------------------------------------------

createTenantYaml.py:  Enable user to load a config file (yaml format) while creating a tenant
usage:
python createTenantYaml.py createTenant.yaml

--------------------------------------------------------------------

CreateTenant_Wizard.py:  a step by step Wizard that helps user to accomplish the tasks in Lab2 in Lab Guide (version 1.19)
