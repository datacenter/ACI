from cobra.model.l3ext import LNodeP, RsNodeL3OutAtt

from createRoutedOutside import input_key_args as input_routed_outside_name
from createNodesAndInterfacesProfile import input_key_args as input_node_profile_name
from utility import *


def input_key_args(msg='\nPlease input the Node Profile info', from_delete_function=False):
    print msg
    key_args = []
    key_args.append(get_raw_input("Leaf ID (required): ", required=True))
    if not from_delete_function:
        key_args.append(get_raw_input("Router ID (required): ", required=True))
    return key_args


def create_node(modir, tenant_name, routed_outside_name, node_profile_name, leaf_id, router_id):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    l3ext_lnodep = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name + '/lnodep-' + node_profile_name)
    if isinstance(l3ext_lnodep, LNodeP):
        l3ext_rsnodel3outatt = RsNodeL3OutAtt(l3ext_lnodep, 'topology/pod-1/node-' + leaf_id, rtrId=router_id)
    else:
        print 'Node and Interface Profile', node_profile_name, 'does not existed.'
        return
    print_query_xml(l3ext_lnodep)
    commit_change(modir, l3ext_lnodep)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'routed_outside', 'help': 'Routed Outside Network Name.'},
                {'name': 'node_profile', 'help': 'Node Profile Name.'},
                {'name': 'leaf_id', 'help': 'Leaf ID.'},
                {'name': 'router_id', 'help': 'Router ID.'}
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Create Node.', key_args)
        tenant_name = args.pop('tenant')
        routed_outside_name = args.pop('routed_outside')
        node_profile_name = args.pop('node_profile')
        leaf_id = args.pop('leaf_id')
        router_id = args.pop('router_id')

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        node_profile_name = input_node_profile_name()
        leaf_id, router_id = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_node(modir, tenant_name, routed_outside_name, node_profile_name, leaf_id, router_id)

    modir.logout()


