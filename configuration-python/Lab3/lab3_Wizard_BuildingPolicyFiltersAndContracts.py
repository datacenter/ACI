import sys
from utility import *
import createFilter
import createContract


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
    filter_array = add_mos_with_options(createFilter.input_key_args, createFilter.input_optional_args, 'Create a Filter')
    contract_array = add_mos_with_options(createContract.input_key_args, createContract.input_optional_args, 'Create a Contract')

    # Running
    for filter in filter_array:
        print filter, filter_array
        createFilter.create_filter(modir, tenant_name, filter[0], args_from_CLI=filter[1])
    for contract in contract_array:
        createContract.create_contract(modir, tenant_name, contract[0], args_from_CLI=contract[1])

    modir.logout()
