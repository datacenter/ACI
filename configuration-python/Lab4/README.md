Lab4
====================

For beginner user, you can simply run the code directly:
eg: python createApplication.py
Then you just need to follow the Wizard to finish the configuration.

====================

For advanced user, you could put all the key arguments and optional arguments when you call the python code.
The format of the key arguments and optional argument for all the codes are list as below:


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

create3TierApplicationLab4.py: a implement code that utilize all the codes under this folder in order to accomplish the tasks in Lab4 in Lab Guide (version 1.19). A user can define the tenant and application names.
usage:
python create3TierApplicationLab4.py <hostname> <username> <password> <tenant_name> <application_name>
python create3TierApplicationLab4.py 172.22.233.207 admin Cisco123 ACILab 3Tier_App

--------------------------------------------------------------------

create3TierApplicationYaml.py: Enable user to load a config file (yaml format) for building an application
usage:
python create3TierApplicationYaml.py create3TierApplication.yaml

--------------------------------------------------------------------

create3TierApplicationWizard.py:  a step by step Wizard that helps user to accomplish the tasks in Lab4 in Lab Guide (version 1.19)
