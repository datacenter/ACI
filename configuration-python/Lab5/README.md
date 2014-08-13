Lab5
====================

addVmmDomainAssociation.py: to associate a VMM domain to an EPG.
usage:
python addVmmDomainAssociation.py <hostname> <username> <password> <tenant_name> <application> <epg> <vmm_domain> [-d deployment-immediacy?] [-r resolution-immediacy?]
python addVmmDomainAssociation.py 172.22.233.207 admin Cisco123 ACILab 3Tier_App Web_EPG vCenter Web_Con -d -r

--------------------------------------------------------------------

createVcenterController.py: to create a vCenter controller.
usage:
python createVcenterController.py <hostname> <username> <password> <vm_provider> <vmm_domain_name> <controller_name> <host_or_ip> <data_center> [-s stats-collection?] [-d <data-center>] [-a <associated-credential>]
python createVcenterController.py 172.22.233.207 admin Cisco123 VMware my_vCenter ACILab 192.168.1.100 ACILab -a administrator

--------------------------------------------------------------------

createVcenterCredential.py: to create a vCenter credential.
usage:
python createVcenterCredential.py <hostname> <username> <password> <vm_provider> <vmm_domain_name> <profile_name> <username> <pw>
python createVcenterCredential.py 172.22.233.207 admin Cisco123 VMware my_vCenter administrator student P@ssw0rd 

--------------------------------------------------------------------

createVlanPool.py: to create a VLAN pool.
usage:
python createVlanPool.py <hostname> <username> <password> <vlan_name> <allocation_mode> <vlan_range_from> <vlan_range_to>
python createVlanPool.py 172.22.233.207 admin Cisco123 ACILab_Vlan_Pool dynamic 1001 1100

--------------------------------------------------------------------

createVmmDomain.py: to create a VMM domain.
usage:
python createVmmDomain.py <hostname> <username> <password> <vm_provider> <VMM_domain_name> [-v <vlan-name>] [-m <vlan-mode>]
python createVmmDomain.py 172.22.233.207 admin Cisco123 VMware my_vCenter -v ACILab_Vlan_Pool -m dynamic

--------------------------------------------------------------------

deleteVcenterController.py: to delete a vCenter controller.
usage:
python disconnectEpgContract.py <hostname> <username> <password> <vm_provider> <vmm_domain_name> <controller_name>
python disconnectEpgContract.py 172.22.233.207 admin Cisco123 VMware my_vCenter my_vCenter ACILab_controller

--------------------------------------------------------------------

deleteVcenterCredential.py: to delete a vCenter Credential.
usage:
python lab4_Create3TierApplication.py <hostname> <username> <password> <vm_provider> <vmm_domain_name> <profile_name>
python lab4_Create3TierApplication.py 172.22.233.207 admin Cisco123 WMware my_vCenter administrator


--------------------------------------------------------------------

deleteVlanPool.py: to delete a VLAN pool.
usage:
python lab4_Create3TierApplication.py <hostname> <username> <password> <vlan_name> <allocation_mode>
python lab4_Create3TierApplication.py 172.22.233.207 admin Cisco123 ACILab_VLAN_Pool dynamic


--------------------------------------------------------------------

deleteVmmDomain.py: to delete a VMM Domain.
usage:
python lab4_Create3TierApplication.py <hostname> <username> <password> <vm_provider> <VMM_domain_name>
python lab4_Create3TierApplication.py 172.22.233.207 admin Cisco123 WMware my_vCenter


--------------------------------------------------------------------

deleteVmmDomainAssociation.py: to take off a VMM Domain from an EPG.
usage:
python lab4_Create3TierApplication.py <hostname> <username> <password> <tenant_name> <application> <epg> <vmm_domain>
python lab4_Create3TierApplication.py 172.22.233.207 admin Cisco123 ACILab 3Tier_app Web_EPG my_vCenter

