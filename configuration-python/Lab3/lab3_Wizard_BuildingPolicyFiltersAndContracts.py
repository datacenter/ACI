import sys
from utility import *
import createFilter
import createContract


# add a MO
def adding_a_mo(msg):
    r_input = raw_input('\n' + msg+' (y/n)? : ')
    if r_input == '':
        adding_a_mo(msg)
    return r_input.lower() in ['yes', 'y']

# add a list the the same type MOs
def add_mos(key_function, optional_function, msg):
    mos = []
    add_one_mo = adding_a_mo(msg)
    msg = msg.replace(' a ', ' another ')
    while add_one_mo:
        new_mo = []
        new_mo.append(key_function())
        new_mo.append(optional_function(new_mo[0]))
        mos.append(new_mo)
        add_one_mo = adding_a_mo(msg)
    return mos


if __name__ == '__main__':

    # Login
    hostname, username, password = '172.22.233.207', 'admin','Cisco123'#input_login_info(msg='')
    try:
        modir = apic_login(hostname, username, password)
        print 'Login succeed.'
    except KeyError:
        print 'Login fail.'
        sys.exit()

    # input Tenant info
    tenant_name = 'bon_python'#input_tenant_name()

    filter_array = add_mos(createFilter.input_key_args, createFilter.input_optional_args, 'Create a Filter')
    contract_array = add_mos(createContract.input_key_args, createContract.input_optional_args, 'Create a Contract')

    for filter in filter_array:
        print filter, filter_array
        createFilter.create_filter(modir, tenant_name, filter[0], args_from_CLI=filter[1])
    for contract in contract_array:
        createContract.create_contract(modir, tenant_name, contract[0], args_from_CLI=contract[1])

    modir.logout()
