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
    if len(sys.argv) != 6:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
        contract_name = input_key_args()
    else:
        hostname, username, password, tenant_name, contract_name = sys.argv[1:]
    modir = apic_login(hostname, username, password)
    delete_contract(modir, tenant_name, contract_name)
    modir.logout()
