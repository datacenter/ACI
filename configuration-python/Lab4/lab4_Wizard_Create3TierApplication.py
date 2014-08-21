import createApplication
import createApplicationEPG
import connectEpgContract

from utility import *

if __name__ == '__main__':

    # Login
    hostname, username, password = input_login_info(msg='')
    try:
        modir = apic_login(hostname, username, password)
        print 'Login succeed.'
    except KeyError:
        print 'Login fail.'
        sys.exit()

    # Wizard starts asking inputs step by step
    tenant_name = input_tenant_name()
    application_name = input_application_name()
    application_option = createApplication.input_optional_args()
    application_epg_array = add_mos_with_options(createApplicationEPG.input_key_args, createApplicationEPG.input_optional_args, 'Create an EPG')
    contracts_array = add_mos(connectEpgContract.input_key_args, 'Add a Provided/consumed Contract')

    # Running
    createApplication.create_application(modir, tenant_name, application_name, args_from_CLI=application_option)
    for application_epg in application_epg_array:
        createApplicationEPG.create_application_epg(modir, tenant_name,application_name, application_epg[0], args_from_CLI=application_epg[1])
    for contract in contracts_array:
        connectEpgContract.connect_epg_contract(modir, tenant_name, application_name, contract[0], contract[1], contract[2])
    modir.logout()
