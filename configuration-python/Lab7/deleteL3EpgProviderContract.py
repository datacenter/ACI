from cobra.model.fv import RsProv

from createRoutedOutside import input_key_args as input_routed_outside_name
from createExternalNetwork import input_key_args as input_external_network_name
from createL3EpgProviderContract import input_key_args

from utility import *


def delete_L3_epg_provider_contract(modir, tenant_name, routed_outside_name, external_network_name, contract_name):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)

    if contract_name == '':
        contract_name = 'default'

    fv_l3epg_rsprov = modir.lookupByDn('uni/tn-'+tenant_name+'/out-'+routed_outside_name+'/instP-'+external_network_name+'/rsprov-'+contract_name)
    if isinstance(fv_l3epg_rsprov, RsProv):
        fv_l3epg_rsprov.delete()
    else:
        print 'L3 EPG Provider Contract', contract_name, 'does not existed.'
        return

    print_query_xml(fv_l3epg_rsprov)
    commit_change(modir, fv_l3epg_rsprov)

if __name__ == '__main__':

    try:
        host_name, user_name, password, tenant_name, routed_outside_name, external_network_name, contract_name = sys.argv[1:8]
    except ValueError:
        host_name, user_name, password = input_login_info() 
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        external_network_name = input_external_network_name()
        contract_name = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_L3_epg_provider_contract(modir, tenant_name, routed_outside_name, external_network_name, contract_name)

    modir.logout()


