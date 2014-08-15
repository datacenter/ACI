from createNodesAndInterfacesProfile import input_key_args
from cobra.model.l3ext import LNodeP

from utility import *


def delete_routed_outside(modir, tenant_name, routed_outside_name, node_profile_name):
    l3ext_lndoep = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name + '/lnodep-' + node_profile_name)
    if isinstance(l3ext_lndoep, LNodeP):
        l3ext_lndoep.delete()
    else:
        print 'Nodes and Interfaces Profile', node_profile_name, 'does not existed.'
    print_query_xml(l3ext_lndoep)
    commit_change(modir, l3ext_lndoep)


if __name__ == '__main__':

    try:
        host_name, user_name, password, tenant_name, routed_outside_name, node_profile_name = sys.argv[1:7]
    except ValueError:
        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name, node_profile_name = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_routed_outside(modir, tenant_name, routed_outside_name, node_profile_name)

    modir.logout()


