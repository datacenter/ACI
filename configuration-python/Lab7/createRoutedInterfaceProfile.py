import getopt
from createRoutedOutside import input_key_args as input_routed_outside_name
from createNodesAndInterfacesProfile import input_key_args as input_node_profile_name
from createInterfaceProfile import input_key_args as input_interface_name
from cobra.model.l3ext import LIfP, RsPathL3OutAtt
from cobra.model.ospf import IfP

from utility import *

import pdb
def input_key_args(msg='\nPlease input the Routed Interface Profile info'):
    print msg
    key_args = []
    key_args.append(get_raw_input("Leaf ID (required): ", required=True))
    key_args.append(get_raw_input("Eth number (required): ", required=True))
    key_args.append(get_raw_input("IP address (required): ", required=True))
    return key_args


def input_optional_args(*arg):
    args = {}
    args['mtu'] = get_optional_input('MTU (default: inherit): ', [], num_accept=True)
    args['targetDscp'] = get_optional_input('Target DSCP (default: "unspecified"): ', [], num_accept=True)
    return args


def create_routed_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name, leaf_id, eth_num, ip_address, **args):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    l3ext_lifp = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name + '/lnodep-' + node_profile_name + '/lifp-' + interface_name)
    if isinstance(l3ext_lifp, LIfP):
        l3ext_rspathl3outatt = RsPathL3OutAtt(l3ext_lifp,
                                    'topology/pod-1/paths-' + leaf_id + '/pathep-[eth' + eth_num + ']',
                                    addr=ip_address,
                                    ifInstT='12',
                                    mtu=get_value(args, 'mtu', 'inherit'),
                                    targetDscp=get_value(args, 'targetDscp', 'unspecified'))
        ospf_ifp = IfP(l3ext_lifp)
    else:
        print 'Interface Profile', interface_name, 'does not existed.'
        return
    print_query_xml(l3ext_lifp)
    commit_change(modir, l3ext_lifp)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    opts = sys.argv[1:]
    opts.reverse()

    # Obtain the key parameters.
    keys = []
    while len(opts) > 0 and opts[len(opts)-1][0] != '-':
        keys.append(opts.pop())
    opts.reverse()

    try:
        host_name, user_name, password, tenant_name, routed_outside_name, node_profile_name, interface_name, leaf_id, eth_num, ip_address = sys.argv[1:11]

        # Obtain the optional arguments that with a flag.
        try:
            opts, args = getopt.getopt(opts, 'M:D:',
                                       ['MTU','target-DSCP='])
        except getopt.GetoptError:
            sys.exit(2)
        optional_args = {}
        for opt, arg in opts:
            if opt in ('-M', '--MTU'):
                optional_args['mtu'] = arg
            elif opt in ('-D', '--target-DSCP'):
                optional_args['targetDscp'] = arg
    except ValueError:
        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        node_profile_name = input_node_profile_name()
        interface_name = input_interface_name()
        leaf_id, eth_num, ip_address = input_key_args()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_routed_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name, leaf_id, eth_num, ip_address, args_from_CLI=optional_args)

    modir.logout()


