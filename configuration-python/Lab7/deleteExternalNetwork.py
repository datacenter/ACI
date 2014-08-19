from cobra.model.l3ext import InstP
from createRoutedOutside import input_key_args as input_routed_outside_name
from createExternalNetwork import input_key_args

from utility import *


def delete_external_network(modir, tenant_name, routed_outside_name, external_network_name):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    l3ext_instp = modir.lookupByDn('uni/tn-'+tenant_name+'/out-'+routed_outside_name+'/instP-'+external_network_name)
    if isinstance(l3ext_instp, InstP):
        l3ext_instp.delete()
    else:
        print 'External Netwrok', external_network_name, 'does not existed.'
        return
    print_query_xml(l3ext_instp)
    commit_change(modir, l3ext_instp)

if __name__ == '__main__':


    try:
        host_name, user_name, password, tenant_name, routed_outside_name, external_network_name = sys.argv[1:7]

    except ValueError:
        host_name, user_name, password = input_login_info() 
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        external_network_name = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_external_network(modir, tenant_name, routed_outside_name, external_network_name)

    modir.logout()


