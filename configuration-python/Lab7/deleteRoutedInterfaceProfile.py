from cobra.model.l3ext import RsPathL3OutAtt
from createRoutedInterfaceProfile import input_key_args

from utility import *


def delete_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name, leaf_id, eth_num, ip_address):
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

    try:
        host_name, user_name, password, tenant_name, routed_outside_name, node_profile_name, interface_name, leaf_id, eth_num, ip_address = sys.argv[1:11]
    except ValueError:
        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name, node_profile_name, interface_name, leaf_id, eth_num, ip_address = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name, leaf_id, eth_num, ip_address)

    modir.logout()


