import createRoutedOutside
import createNodesAndInterfacesProfile
import createNodes
import createInterfaceProfile
import createRoutedInterfaceProfile
import createExternalNetwork

from utility import *
import pdb

if __name__ == '__main__':

    # Login
    hostname, username, password = '172.22.233.207', 'admin', 'Cisco123'  # input_login_info(msg='')
    try:
        modir = apic_login(hostname, username, password)
        print 'Login succeed.'
    except KeyError:
        print 'Login fail.'
        sys.exit()

    # Wizard starts asking inputs step by step
    tenant_name = input_tenant_name()
    routed_outside_name = createRoutedOutside.input_key_args()
    routed_outside_optional_args = createRoutedOutside.input_optional_args()
    node_profile_name = createNodesAndInterfacesProfile.input_key_args()
    node_profile_optional_args = createNodesAndInterfacesProfile.input_optional_args()
    nodes_array = add_mos(createNodes.input_key_args, 'Create a Node')
    interface_name = createInterfaceProfile.input_key_args()
    routed_interface_array = add_mos_with_options(createRoutedInterfaceProfile.input_key_args, createRoutedInterfaceProfile.input_optional_args, 'Add a Routed Interface')
    external_network = createExternalNetwork.input_key_args()
    external_network_optional_args = createExternalNetwork.input_optional_args()

    # Running
    createRoutedOutside.create_routed_outside(modir, tenant_name, routed_outside_name, args_from_CLI=routed_outside_optional_args)
    createNodesAndInterfacesProfile.create_node_profile(modir, tenant_name, routed_outside_name, node_profile_name, args_from_CLI=node_profile_optional_args)
    for node in nodes_array:
        createNodes.create_node(modir, tenant_name, routed_outside_name, node_profile_name, node[0], node[1])
    createInterfaceProfile.create_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name)
    for routed_interface in routed_interface_array:
        createRoutedInterfaceProfile.create_routed_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name, routed_interface[0][0], routed_interface[0][1], routed_interface[0][2], args_from_CLI=routed_interface[1])
    createExternalNetwork.create_external_network(modir, tenant_name, routed_outside_name, external_network, args_from_CLI=external_network_optional_args)



