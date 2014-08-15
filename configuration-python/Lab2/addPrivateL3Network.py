import sys
from utility import *
from cobra.model.fv import Ctx


def input_key_args(msg='Please input Private L3 Network info:'):
    print msg
    return get_raw_input("Private L3 Network (required): ", required=True)


def add_private_l3_network(modir, tenant_name, private_l3_network):
    """Build a private L3 network"""

    # Query a tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)

    # create a private network
    fv_ctx = Ctx(fv_tenant, private_l3_network)

    print_query_xml(fv_tenant)
    commit_change(modir, fv_tenant)

if __name__ == '__main__':
    if len(sys.argv) != 6:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
        private_l3_network = input_key_args()
    else:
        hostname, username, password, tenant_name, private_l3_network = sys.argv[1:]

    modir = apic_login(hostname, username, password)
    add_private_l3_network(modir, tenant_name, private_l3_network)
    modir.logout()
