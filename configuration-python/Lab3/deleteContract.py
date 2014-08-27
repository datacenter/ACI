from createContract import input_key_args, BrCP
from utility import *


def delete_contract(modir, tenant_name, contract_name):
    """Delete a contract"""

    # Check if the contract exists or not. If yes, delete it.
    vz_brcp = modir.lookupByDn('uni/tn-' + tenant_name + '/brc-' + contract_name)
    if isinstance(vz_brcp, BrCP):
        vz_brcp.delete()
    else:
        print 'There is no contract called', contract_name, 'in tenant' , tenant_name, '.'
        return

    print_query_xml(vz_brcp)
    commit_change(modir, vz_brcp)


if __name__ == '__main__':

    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'contract', 'help': 'Contract name'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Create a Contract.', key_args)
        tenant_name = args.pop('tenant')
        contract_name = args.pop('contract')

    except:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        try:
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            tenant_name = data['tenant']
            contract_name = data['contract']
        except (IOError, KeyError, TypeError, IndexError):
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            contract_name = input_key_args()

    modir = apic_login(host_name, user_name, password)
    delete_contract(modir, tenant_name, contract_name)
    modir.logout()
