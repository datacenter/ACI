from cobra.model.l3ext import LNodeP, LIfP
from createInterfaceProfile import input_key_args

from utility import *


def delete_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    l3ext_lifp = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name + '/lnodep-' + node_profile_name + '/lifp-' + interface_name)
    if isinstance(l3ext_lifp, LIfP):
        l3ext_lifp.delete()
    else:
        print 'Interface Profile', interface_name, 'does not existed.'
        return
    print_query_xml(l3ext_lifp)
    commit_change(modir, l3ext_lifp)


if __name__ == '__main__':

    try:
        host_name, user_name, password, tenant_name, routed_outside_name, node_profile_name, interface_name = sys.argv[1:9]
    except ValueError:
        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name, node_profile_name, interface_name = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name)

    modir.logout()


