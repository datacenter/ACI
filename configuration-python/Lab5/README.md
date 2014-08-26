Lab5
====================

For beginner user, you can simply run the code directly:
eg: python createVcenterController.py
Then you just need to follow the Wizard to finish the configuration.

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
python deleteVcenterController.py <hostname> <username> <password> <vm_provider> <vmm_domain_name> <controller_name>
python deleteVcenterController.py 172.22.233.207 admin Cisco123 VMware my_vCenter ACILab_controller

--------------------------------------------------------------------

deleteVcenterCredential.py: to delete a vCenter Credential.
usage:
python deleteVcenterCredential.py <hostname> <username> <password> <vm_provider> <vmm_domain_name> <profile_name>
python deleteVcenterCredential.py 172.22.233.207 admin Cisco123 WMware my_vCenter administrator


--------------------------------------------------------------------

deleteVlanPool.py: to delete a VLAN pool.
usage:
python deleteVlanPool.py <hostname> <username> <password> <vlan_name> <allocation_mode>
python deleteVlanPool.py 172.22.233.207 admin Cisco123 ACILab_VLAN_Pool dynamic


--------------------------------------------------------------------

deleteVmmDomain.py: to delete a VMM Domain.
usage:
python deleteVmmDomain.py <hostname> <username> <password> <vm_provider> <VMM_domain_name>
python deleteVmmDomain.py 172.22.233.207 admin Cisco123 WMware my_vCenter


--------------------------------------------------------------------

deleteVmmDomainAssociation.py: to take off a VMM Domain from an EPG.
usage:
python deleteVmmDomainAssociation.py <hostname> <username> <password> <tenant_name> <application> <epg> <vmm_domain>
python deleteVmmDomainAssociation.py 172.22.233.207 admin Cisco123 ACILab 3Tier_app Web_EPG my_vCenter

--------------------------------------------------------------------

intergratingWithVMwareLab5.py: a implement code that utilize all the codes under this folder in order to accomplish the tasks in Lab5 in Lab Guide (version 1.19)
usage:
python intergratingWithVMwareLab5.py <hostname> <username> <password> <tenant_name> <application_name>
python intergratingWithVMwareLab5.py 172.22.233.207 admin Cisco123 ACILab 3Tier_App

--------------------------------------------------------------------

intergratingWithVMwareYaml.py: Enable user to Enable user to load a config file (yaml format) for integrating application EPG with VMware
usage:
python intergratingWithVMwareYaml.py intergratingWithVMware.yaml

--------------------------------------------------------------------

layer3ExternalWizard.py:  a step by step Wizard that helps user to accomplish the tasks in Lab3 in Lab Guide (version 1.19)
