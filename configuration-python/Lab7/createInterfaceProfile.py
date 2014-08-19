from createRoutedOutside import input_key_args as input_routed_outside_name
from createNodesAndInterfacesProfile import input_key_args as input_node_profile_name
from cobra.model.l3ext import LNodeP, LIfP

from utility import *


def input_key_args(msg='\nPlease input the Interface Profile info'):
    print msg
    return get_raw_input("Interface Name (required): ", required=True)


def create_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    l3ext_lnodep = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name + '/lnodep-' + node_profile_name)
    if isinstance(l3ext_lnodep, LNodeP):
        l3ext_lifp = LIfP(l3ext_lnodep, interface_name)
    else:
        print 'Node and Interface Profile', node_profile_name, 'does not existed.'
        return

    print_query_xml(l3ext_lnodep)
    commit_change(modir, l3ext_lnodep)


if __name__ == '__main__':

    try:
        host_name, user_name, password, tenant_name, routed_outside_name, node_profile_name, interface_name = sys.argv[1:9]
    except ValueError:
        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        node_profile_name = input_node_profile_name()
        interface_name = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name)

    modir.logout()


