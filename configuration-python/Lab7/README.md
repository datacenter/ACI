Lab7
====================

For beginner user, you can simply run the code directly:
eg: python createTenant.py
Then you just need to follow the Wizard to finish the configuration.

====================

For advanced user, you could put all the key arguments and optional arguments when you call the python code.
The format of the key arguments and optional argument for all the codes are list as below:


associateL3OutsideNetworkToBD.py: to associate the L3 Outside network to a Bridge Domain.
usage:
python associateL3OutsideNetworkToBD.py <hostname> <username> <password> <tenant_name> <bridge_domain> <external_network_name>
python associateL3OutsideNetworkToBD.py 172.22.233.207 admin Cisco123 ACILab ACILab_BD1 ACILab_VRF

--------------------------------------------------------------------

configPrivateL3NetworkDefaultTimers.py: Set Setting for Private Network
usage:
python configPrivateL3NetworkDefaultTimers.py <hostname> <username> <password> <tenant_name> <private_network> [-B <BGP_timer>] [-O <OSPF_timer>] [-e End <point_retention_policy>] [-m <monitoring_olicy>]
python configPrivateL3NetworkDefaultTimers.py 172.22.233.207 admin Cisco123 ACILab ACILab_VRF -O default

--------------------------------------------------------------------

createBgpRouteReflector.py: set a spine as BGP Route Reflector
usage:
python createBgpRouteReflector.py <hostname> <username> <password> <spin_id>
python createBgpRouteReflector.py 172.22.233.207 admin Cisco123 102

--------------------------------------------------------------------

createExternalNetwork.py: configure External EPG Network
usage:
python createExternalNetwork.py <hostname> <username> <password> <tenant_name> <routed_outside_name> <external_network_name> [-Q <QoS_class>] [-s <subnet_ip>] 
python createExternalNetwork.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out L3-Out-EPG -Q unspecified -s 0.0.0.0/0

--------------------------------------------------------------------

createInterfaceProfile.py: configure OSPF Interface Profile
usage:
python createInterfaceProfile.py <hostname> <username> <password> <tenant_name> <routed_outside_name> <interface_name>
python createInterfaceProfile.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out L3-OSPF-Leaf2

--------------------------------------------------------------------

createL3EpgConsumerContract.py: configure consumer for Routed Outside Network
usage:
python createL3EpgConsumerContract.py <hostname> <username> <password> <tenant_name> <routed_outside_name> <external_network_name> <contract_name> [-Q <QoS_class>]
python createL3EpgConsumerContract.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out L3-Out-EPG default -Q unspecified

--------------------------------------------------------------------

createL3EpgProviderContract.py: configure provider for Routed Outside Network
usage:
python createL3EpgProviderContract.py <hostname> <username> <password> <tenant_name> <routed_outside_name> <external_network_name> <contract_name> [-Q <QoS_class>] [-m <match_type>]
python createL3EpgProviderContract.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out L3-Out-EPG default -Q unspecified -m AtleastOne

--------------------------------------------------------------------

createNodes.py: Create External Node Profile
usage:
python createNodes.py <hostname> <username> <password> <tenant_name> <routed_outside_name> <node_profile_name> <leaf_id> <router_id>
python createNodes.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out Border-Leaf2 102 1.0.0.2

--------------------------------------------------------------------

createNodesAndInterfacesProfile.py: Configure Border Node
usage:
python createNodesAndInterfacesProfile.py <hostname> <username> <password> <tenant_name> <routed_outside_name> <node_profile_name> [-D <target_DSCP>]
python createNodesAndInterfacesProfile.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out Border-Leaf2 -D 1

--------------------------------------------------------------------

createPodPolicyGroup.py: configure Pod Policy Group
usage:
python createPodPolicyGroup.py <hostname> <username> <password> <policy_group_name> [-d Date Time_policy?] [-I ISIS_policy?] [-C COOP_group_poicy?] [-B BGP_route_reflector_policy?] [-c communication_policy?] [-S SNMP_policy] 
python createPodPolicyGroup.py 172.22.233.207 admin Cisco123 PodPolicy -B

--------------------------------------------------------------------

createRoutedInterfaceProfile.py: configure Routed Interface
usage:
python createRoutedInterfaceProfile.py <hostname> <username> <password> <tenant_name> <routed_outside_name> <node_profile_name> <interface_name> <leaf_id> <eth_num> <ip_address> [-M <MTU>] [-D <target_DSCP>]
python createRoutedInterfaceProfile.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out Border-Leaf2 L3-OSPF-Leaf2 102 1/1 30.30.30.1/24 -M 1500

--------------------------------------------------------------------

createRoutedOutside.py: configure L3 Routed Outside
usage:
python createRoutedOutside.py <hostname> <username> <password> <tenant_name> <routed_outside_name> [-n <private_network>] [-t <tags>] [-B BGP?] [-O OSPF?] [-i OSPF_id]
python createRoutedOutside.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out -n ACILab_VRF -O -i 1

--------------------------------------------------------------------

setAutonomousSystemNumber.py: set Autonomous System Number
usage:
python setAutonomousSystemNumber.py <hostname> <username> <password> <autonomous_system_number>
python setAutonomousSystemNumber.py 172.22.233.207 admin Cisco123 1

--------------------------------------------------------------------

selectPodPolicy.py: select a Pod Policy
usage:
python selectPodPolicy.py <hostname> <username> <password> <policy_group>
python selectPodPolicy.py 172.22.233.207 admin Cisco123 PodPolicy

--------------------------------------------------------------------

deleteBgpRouteReflector.py: to remove a BGP Route Reflector
usage:
python deleteBgpRouteReflector.py <hostname> <username> <password> <spine_id>
python deleteBgpRouteReflector.py 172.22.233.207 admin Cisco123 102

--------------------------------------------------------------------
deleteExternalNetwork.py: delete a External EPG Network
usage:
python deleteExternalNetwork.py <hostname> <username> <password> <tenant_name> <routed_outside_name> <external_network_name>
python deleteExternalNetwork.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out L3-Out-EPG

--------------------------------------------------------------------

deleteNodes.py: delete External Node Profile.
usage:
python deleteNodes.py <hostname> <username> <password> <tenant_name> <routed_outside_name> <node_profile_name> <leaf_id>
python deleteNodes.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out Border-Leaf2 102

--------------------------------------------------------------------

deleteNodesAndInterfacesProfile.py: to delete a Border Node.
usage:
python deleteNodesAndInterfacesProfile.py <hostname> <username> <password> <tenant_name> <routed_outside_name> <node_profile_name>
python deleteNodesAndInterfacesProfile.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out Border-Leaf2

--------------------------------------------------------------------

deletePodPolicyGroup.py: to delete a Pod Policy Group.
usage:
python deletePodPolicyGroup.py <hostname> <username> <password> <policy_name>
python deletePodPolicyGroup.py 172.22.233.207 admin Cisco123 PodPolicy

--------------------------------------------------------------------

deleteRoutedInterfaceProfile.py: to delete a Routed Interface.
usage:
python deleteRoutedInterfaceProfile.py <hostname> <username> <password> <tenant_name> <routed_outside_name> <node_profile_name> <interface_name> <leaf_id> <eth_num> 
python deleteRoutedInterfaceProfile.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out Border-Leaf2 L3-OSPF-Leaf2 102 1/1

--------------------------------------------------------------------

deleteRoutedOutside.py: to delete a L3 Routed Outside.
usage:
python deleteRoutedOutside.py <hostname> <username> <password> <tenant_name> <routed_outside_name>
python deleteRoutedOutside.py 172.22.233.207 admin Cisco123 ACILab ACILab-L3-Out

--------------------------------------------------------------------

deselectPodPolicy.py: deselect a Pod Policy.
usage:
python deselectPodPolicy.py <hostname> <username> <password> 
python deselectPodPolicy.py 172.22.233.207 admin Cisco123

--------------------------------------------------------------------

disassociateL3OutsideNetworkToBD.py: to disassociate the L3 Outside network to a Bridge Domain.
usage:
python disassociateL3OutsideNetworkToBD.py <hostname> <username> <password> <tenant_name> <bridge_domain> <routed_outside_name> 
python disassociateL3OutsideNetworkToBD.py 172.22.233.207 admin Cisco123 ACILab ACILab_BD1 ACILab-L3-Out

--------------------------------------------------------------------

resetAutonomousSystemNumber.py: reset Autonomous System Number
usage:
python setAutonomousSystemNumber.py <hostname> <username> <password>
python setAutonomousSystemNumber.py 172.22.233.207 admin Cisco123

--------------------------------------------------------------------

layer3ExternalLab7A.py: a implement code that utilize all the codes under this folder in order to accomplish the first one third tasks in Lab7 in Lab Guide (version 1.19)
usage:
python layer3ExternalLab7A.py <hostname> <username> <password> <pod_policy>
python layer3ExternalLab7A.py 172.22.233.207 admin Cisco123 PodPolicy

--------------------------------------------------------------------

routedL3ExternalNetworkLab7B.py: a implement code that utilize all the codes under this folder in order to accomplish the second one third tasks in Lab7 in Lab Guide (version 1.19)
usage:
python routedL3ExternalNetworkLab7B.py <hostname> <username> <password> <tenant_name>
python routedL3ExternalNetworkLab7B.py 172.22.233.207 admin Cisco123 ACILab

--------------------------------------------------------------------

setupL3OutNetworkAndBDLab7C.py: a implement code that utilize all the codes under this folder in order to accomplish the last one third tasks in Lab7 in Lab Guide (version 1.19)
usage:
python setupL3OutNetworkAndBDLab7C.py <hostname> <username> <password> <tenant_name>
python setupL3OutNetworkAndBDLab7C.py 172.22.233.207 admin Cisco123 ACILab

--------------------------------------------------------------------

layer3ExternalYaml.py: Enable user to Enable user to load a config file (yaml format) for configuring fabric pod policy
usage:
python layer3ExternalYaml.py layer3External.yaml

--------------------------------------------------------------------

routedL3ExternalNetworkYaml.py: Enable user to Enable user to load a config file (yaml format) for configuring routed L3 external network
usage:
python routedL3ExternalNetworkYaml.py routedL3ExternalNetwork.yaml

--------------------------------------------------------------------

setupL3OutNetworkAndBD.py: Enable user to Enable user to load a config file (yaml format) in order to configure provider/consumer for external network epg, set setting for private network and associate the l3 outside network to a bridge domain
usage:
python setupL3OutNetworkAndBDYaml.py setupL3OutNetworkAndBD.yaml

--------------------------------------------------------------------

layer3ExternalWizard.py:  a step by step Wizard that helps user to configure fabric pod policy
routedL3ExternalNetworkWizard.py:  a step by step Wizard that helps user to configure routed L3 external network
setupL3OutNetworkAndBDWizard.py:  a step by step Wizard that helps user to configure provider/consumer for external network epg, set setting for private network and associate the l3 outside network to a bridge domain

