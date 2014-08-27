from cobra.model.l3ext import RsNodeL3OutAtt
from utility import *


def input_key_args(msg='\nPlease input the Node Profile info'):
    print msg
    key_args = []
    key_args.append(get_raw_input("External Routed Network Name (required): ", required=True))
    key_args.append(get_raw_input("Node Profile Name (required): ", required=True))
    key_args.append(get_raw_input("Leaf ID (required): ", required=True))
    return key_args


def delete_node_profile(modir, tenant_name, routed_outside_name, node_profile_name, leaf_id):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    l3ext_rsnodel3outatt = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name + '/lnodep-' + node_profile_name + '/rsnodeL3OutAtt-[topology/pod-1/node-' + leaf_id + ']')
    if isinstance(l3ext_rsnodel3outatt, RsNodeL3OutAtt):
        l3ext_rsnodel3outatt.delete()
    else:
        print 'Node', '[topology/pod-1/node-' + leaf_id + ']', 'does not existed.'
        return
    print_query_xml(l3ext_rsnodel3outatt)
    commit_change(modir, l3ext_rsnodel3outatt)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'routed_outside', 'help': 'Routed Outside Network Name.'},
                    {'name': 'node_profile', 'help': 'Node Profile Name.'},
                    {'name': 'leaf_id', 'help': 'Leaf ID.'},
        ]

        host_name, user_name, password, args = set_cli_argparse('Delete Node.', key_args)
        tenant_name = args.pop('tenant')
        routed_outside_name = args.pop('routed_outside')
        node_profile_name = args.pop('node_profile')
        leaf_id = args.pop('leaf_id')

    except: #?error

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name, node_profile_name, leaf_id = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_node_profile(modir, tenant_name, routed_outside_name, node_profile_name, leaf_id)

    modir.logout()


