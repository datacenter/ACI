Lab2
====================

addSecurityDomain: to add security domains: such as "all" and "mgmt" to a tenant.
usage:
python addSecurityDomain.py <hostname> <username> <password> <tenant_name> <security_domain>
python addSecurityDomain.py 123.45.678.900 admin cisco123 ACILab all

--------------------------------------------------------------------

buildBridgeDomainSubnet: to build a bridge domain and its associated a subnet. The bridge domain should connect to a private network (which is build by running buildPrivateL3Network). 
usage:
python buildBridgeDomainSubnet.py <hostname> <username> <password> <tenant_name> <bridge_domain> <subnet_ip> <network_name>
python buildBridgeDomainSubnet.py 123.45.678.900 admin cisco123 ACILab ACILab_BD1 10.10.10.1/24 ACILab_VRF

--------------------------------------------------------------------

buildPrivateL3Network: to build a private level 3 network (context). It shall contain one bridge domain.
usage:
python buildPrivateL3Network.py <hostname> <username> <password> <tenant_name> <network_name>
python buildPrivateL3Network.py 123.45.678.900 admin cisco123 ACILab ACILab_VRF

--------------------------------------------------------------------

createTenant: to create a tenant.
usage:
python createTenant.py <hostname> <username> <password> <tenant_name>
python createTenant.py 123.45.678.900 admin cisco123 ACILab

--------------------------------------------------------------------

deleteBridgeDomain: to delete a bridge domain.
usage:
python deleteBridgeDomain.py <hostname> <username> <password> <tenant_name> <bridge_domain>
python deleteBridgeDomain.py 123.45.678.900 admin cisco123 ACILab ACILab_BD1

--------------------------------------------------------------------

deletePrivateL3Network: to delete a private level 3 network.
usage:
python deletePrivateL3Network.py <hostname> <username> <password> <tenant_name> <network_name>
python deletePrivateL3Network.py 123.45.678.900 admin cisco123 ACILab ACILab_VRF

--------------------------------------------------------------------

deleteTenant: to delete a tenant.
usage:
python deleteTenant.py <hostname> <username> <password> <tenant_name>
python deleteTenant.py 123.45.678.900 admin cisco123 ACILab

--------------------------------------------------------------------

lab2_CreateTenant:  a implement code that utilize all the codes under this folder in order to accomplish the tasks in Lab2 in Lab Guide (version 19)
usage:
python lab2_CreateTenant.py <hostname> <username> <password> <tenant_name>
python lab2_CreateTenant.py 123.45.678.900 admin cisco123 ACILab
