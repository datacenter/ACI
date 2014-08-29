from cobra.model.l3ext import RsPathL3OutAtt
from createRoutedOutside import input_key_args as input_routed_outside_name
from createNodesAndInterfacesProfile import input_key_args as input_node_profile_name
from createInterfaceProfile import input_key_args as input_interface_name
from createRoutedInterfaceProfile import input_key_args

from utility import *


def delete_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name, leaf_id, eth_num):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    l3ext_rspathl3outatt = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name + '/lnodep-' + node_profile_name + '/lifp-' + interface_name + '/rspathL3OutAtt-[topology/pod-1/paths-' + leaf_id + '/pathep-[eth' + eth_num + ']]')
    if isinstance(l3ext_rspathl3outatt, RsPathL3OutAtt):
        l3ext_rspathl3outatt.delete()
    else:
        print 'Such a Routed Interface does not existed.'
        return
    print_query_xml(l3ext_rspathl3outatt)
    commit_change(modir, l3ext_rspathl3outatt)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'routed_outside', 'help': 'Routed Outside Network Name.'},
                {'name': 'node_profile', 'help': 'Node Profile Name.'},
                {'name': 'interface', 'help': 'Interface Name.'},
                {'name': 'leaf_id', 'help': 'Leaf ID.'},
                {'name': 'eth_num', 'help': 'Eth number.'},
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Delete a Routed Interface Profile.', key_args)
        tenant_name = args.pop('tenant')
        routed_outside_name = args.pop('routed_outside')
        node_profile_name = args.pop('node_profile')
        interface_name = args.pop('interface')
        leaf_id = args.pop('leaf_id')
        eth_num = args.pop('eth_num')

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        node_profile_name = input_node_profile_name()
        interface_name = input_interface_name()
        leaf_id, eth_num, ip_address = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name, leaf_id, eth_num)

    modir.logout()


