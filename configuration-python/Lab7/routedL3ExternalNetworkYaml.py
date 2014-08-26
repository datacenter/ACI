from createRoutedOutside import create_routed_outside
from createNodesAndInterfacesProfile import create_node_profile
from createNodes import create_node
from createInterfaceProfile import create_interface_profile
from createRoutedInterfaceProfile import create_routed_interface_profile
from createExternalNetwork import create_external_network

from utility import *


if __name__ == '__main__':

    try:
        data = read_config_yaml_file(sys.argv[1], login_info=False)
    except IOError:
        print 'No such file or directory:', sys.argv[1]
        sys.exit()
    else:
        host, user, password = get_login_info(data)
        modir = apic_login(host, user, password)
        tenant = data['tenant']
        routed_outside = data['outside_network']['name']

        routed_outside_opt_args = {}
        routed_outside_opt_args['tnFvCtxName'] = data['outside_network']['private_network']
        routed_outside_opt_args['tags'] = data['outside_network']['tags']
        routed_outside_opt_args['BGP'] = data['outside_network']['applied_bgp']
        routed_outside_opt_args['OSPF'] = data['outside_network']['applied_ospf']
        if routed_outside_opt_args['OSPF']:
            routed_outside_opt_args['areaId'] = str(data['outside_network']['ospf_area_id'])

        node_profile = data['node_profile']['name']
        node_profile_dscp = data['node_profile']['target_dscp']

        leaf_id = str(data['leaf_id'])
        router_id = str(data['router_id'])

        interface = data['interface']['name']
        eth_number = data['interface']['eth_number']
        ip_address = data['interface']['ip_address']
        interface_opt_args = {}
        interface_opt_args['mtu'] = data['interface']['mtu']
        interface_opt_args['targetDscp'] = data['interface']['target_dscp']

        externmal_network_egp = data['external_network_epg']['name']
        externmal_network_egp_opt_args = {}
        externmal_network_egp_opt_args['prio'] = \
            data['external_network_epg']['qos_class']
        externmal_network_egp_opt_args['subnet_ip'] = \
            data['external_network_epg']['subnet_ip']

    # Create Routed Outside
    create_routed_outside(modir, tenant, routed_outside,
                          args_from_CLI=routed_outside_opt_args)

    # Create Node Profile
    create_node_profile(modir, tenant, routed_outside, node_profile,
                        targetDscp=node_profile_dscp)

    # Select Node
    create_node(modir, tenant, routed_outside, node_profile, leaf_id,
                router_id)

    # Create OSPF Interface Profile
    create_interface_profile(modir, tenant, routed_outside, node_profile,
                             interface)

    # Create Routed_Interface
    create_routed_interface_profile(modir, tenant, routed_outside,
                                    node_profile, interface, leaf_id,
                                    eth_number, ip_address,
                                    args_from_CLI=interface_opt_args)

    # Create External EPG Network
    create_external_network(modir, tenant, routed_outside,
                            externmal_network_egp,
                            args_from_CLI=externmal_network_egp_opt_args)

