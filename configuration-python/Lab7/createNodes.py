from cobra.model.l3ext import LNodeP, RsNodeL3OutAtt

from utility import *


def input_key_args(msg='\nPlease input the Node Profile info'):
    print msg
    key_args = []
    key_args.append(get_raw_input("External Routed Network Name (required): ", required=True))
    key_args.append(get_raw_input("Node Profile Name (required): ", required=True))
    key_args.append(get_raw_input("Leaf ID (required): ", required=True))
    key_args.append(get_raw_input("Router ID (required): ", required=True))
    return key_args


def create_node_profile(modir, tenant_name, routed_outside_name, node_profile_name, leaf_id, router_id):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    l3ext_lnodep = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name + '/lnodep-' + node_profile_name)
    if isinstance(l3ext_lnodep, LNodeP):
        l3ext_rsnodel3outatt = RsNodeL3OutAtt(l3ext_lnodep, 'topology/pod-1/node-' + leaf_id, rtrId=router_id)
    else:
        print 'Node and Interface Profile', node_profile_name, 'does not existed.'
    print_query_xml(l3ext_lnodep)
    commit_change(modir, l3ext_lnodep)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    opts = sys.argv[1:]
    opts.reverse()

    # Obtain the key parameters.
    keys = []
    while len(opts) > 0 and opts[len(opts) - 1][0] != '-':
        keys.append(opts.pop())
    opts.reverse()

    try:
        host_name, user_name, password, tenant_name, routed_outside_name, node_profile_name, leaf_id, router_id = sys.argv[1:10]
    except ValueError:
        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name, node_profile_name, leaf_id, router_id = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_node_profile(modir, tenant_name, routed_outside_name, node_profile_name, leaf_id, router_id)

    modir.logout()


