Lab3
====================

createContract: to create a contract.
usage:
python createContract.py <hostname> <username> <password> <tenant_name> <contract_name> [-s <scope>] [-n <contract_subject_name>] [-r reverse_filter_port?] [-Q <QoS_class>] [-f <filter_name>]
python createContract.py 172.22.233.207 admin Cisco123 ACILab Web_Con -s context -n Web_subj -r -Q level2 -f Web_Filter

--------------------------------------------------------------------

createFilter: to create a filter.
usage:
python createFilter.py <hostname> <username> <password> <tenant_name> <filter_name> [-a apply-frag?] [-n <entry_name>] [-e <ether_type>] [-i <ip-protocol>] [-s <source_port_from>] [-S <source_port_to>] [-d <destination_port_from>] [-D <destination_port_to>] [-f <tcp_flag>]
python createFilter.py 172.22.233.207 admin Cisco123 ACILab Web_Filter -a -n web_filter -e ip -i tcp -s http -S http -d http -D http -f finish 

--------------------------------------------------------------------

deleteContract: to delete a contract.
usage:
python deleteContract.py <hostname> <username> <password> <tenant_name> <contract_name>
python deleteContract.py 172.22.233.207 admin Cisco123 ACILab Web_Con

--------------------------------------------------------------------

deleteFilter: to delete a filter.
usage:
python deleteFilter.py <hostname> <username> <password> <tenant_name> <filter_name>
python deleteFilter.py 172.22.233.207 admin Cisco123 ACILab Web_Filter

--------------------------------------------------------------------

lab3_BuildingPolicyFiltersAndContracts: a implement code that utilize all the codes under this folder in order to accomplish the tasks in Lab3 in Lab Guide (version 19)
usage:
python lab3_BuildingPolicyFiltersAndContracts.py <hostname> <username> <password> <tenant_name>
python lab3_BuildingPolicyFiltersAndContracts.py 172.22.233.207 admin Cisco123 ACILab


