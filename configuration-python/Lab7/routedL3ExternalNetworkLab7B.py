from createRoutedOutside import create_routed_outside
from createNodesAndInterfacesProfile import create_node_profile
from createNodes import create_node
from createInterfaceProfile import create_interface_profile
from createRoutedInterfaceProfile import create_routed_interface_profile
from createExternalNetwork import create_external_network

from utility import *

ROUTED_OUTSIDE_NETWORK = 'L3-Out'
PRIVATE_NETWROK = 'VRF'
LEAF_NAME = 'Leaf2'
NODE_PROFILE_NAME = 'Border-' + LEAF_NAME
LEAF_ID = '102'
ROUTED_ID = '1.0.0.2'
MTU = '1500'
INTERFACE_NAME = 'L3-OSPF-' + LEAF_NAME
ETH = '1/1'
IP_ADDRESS = '30.30.30.1/24'
EXTERNAL_NETWORK_NAME = 'L3-Out-EPG'
SUBNET_ID = '0.0.0.0/0'


def lab7B(modir, tenant_name):
    """Setup the Pod Policies"""

    routed_outside_name = tenant_name+'-'+ROUTED_OUTSIDE_NETWORK

    # Create Routed Outside
    create_routed_outside(modir, tenant_name, routed_outside_name, OSPF=True, tnFvCtxName=tenant_name+'_'+PRIVATE_NETWROK)
    # Create Node Profile
    create_node_profile(modir, tenant_name, routed_outside_name, NODE_PROFILE_NAME,)
    # Select Node
    create_node(modir, tenant_name, routed_outside_name, NODE_PROFILE_NAME, LEAF_ID, ROUTED_ID)
    # Create OSPF Interface Profile
    create_interface_profile(modir, tenant_name, routed_outside_name, NODE_PROFILE_NAME, INTERFACE_NAME)
    # Create Routed_Interface
    create_routed_interface_profile(modir, tenant_name, routed_outside_name, NODE_PROFILE_NAME, INTERFACE_NAME, LEAF_ID, ETH, IP_ADDRESS, mtu=MTU)
    # Create External EPG Network
    create_external_network(modir, tenant_name, routed_outside_name, EXTERNAL_NETWORK_NAME, subnet_ip=SUBNET_ID)

if __name__ == '__main__':

    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'}]
        host_name, user_name, password, args = set_cli_argparse('Create a default tenant.', key_args)
        tenant_name = args.pop('tenant')

    except: #?error

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()

    modir = apic_login(host_name, user_name, password)
    lab7B(modir, tenant_name)
    modir.logout()
