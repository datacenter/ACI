Lab4
====================

connectEpgContract: to apply a consumed/provided contract to an EPG.
usage:
python connectEpgContract.py <hostname> <username> <password> <tenant_name> <application_name> <EPG_name> <contract_type> <contract_name>
python connectEpgContract.py 172.22.233.207 admin Cisco123 ACILab 3Tier_App Web_EPG consumed Web_Con

--------------------------------------------------------------------

createApplication: to set up an application profile.
usage:
python createApplication.py <hostname> <username> <password> <tenant_name> <application_name> [-Q <QoS_class>]
python createApplication.py 172.22.233.207 admin Cisco123 ACILab 3Tier_App -Q level2

--------------------------------------------------------------------

createApplicationEPG: to create EPG in an application profile.
usage:
python createApplicationEPG.py <hostname> <username> <password> <tenant_name> <application_name> <EPG_name> [-Q <QoS_class>] [-b <bridge_domain>]
python createApplicationEPG.py 172.22.233.207 admin Cisco123 ACILab 3Tier_App Web_EPG -Q level1 -b ACILab_BD1 

--------------------------------------------------------------------

deleteApplication: to delete an application profile.
usage:
python deleteApplication.py <hostname> <username> <password> <tenant_name> <application_name>
python deleteApplication.py 172.22.233.207 admin Cisco123 ACILab 3Tier_App

--------------------------------------------------------------------

deleteApplicationEPG: to delete an EPG.
usage:
python deleteApplicationEPG.py <hostname> <username> <password> <tenant_name> <application_name> <EPG_name>
python deleteApplicationEPG.py 172.22.233.207 admin Cisco123 ACILab 3Tier_App Web_EPG

--------------------------------------------------------------------

disconnectEpgContract: to un-apply a contract from an EPG.
usage:
python disconnectEpgContract.py <hostname> <username> <password> <tenant_name> <application_name> <EPG_name> <contract_type> <contract_name>
python disconnectEpgContract.py 172.22.233.207 admin Cisco123 ACILab 3Tier_App Web_EPG provided Web_Con

--------------------------------------------------------------------

lab4_Create3TierApplication: a implement code that utilize all the codes under this folder in order to accomplish the tasks in Lab4 in Lab Guide (version 1.19)
usage:
python lab4_Create3TierApplication.py <hostname> <username> <password> <tenant_name> <application_name>
python lab4_Create3TierApplication.py 172.22.233.207 admin Cisco123 ACILab 3Tier_App

