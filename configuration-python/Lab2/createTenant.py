import sys
from utility import *
from cobra.model.fv import Tenant


def create_tenant(modir, tenant_name):
    """Create a tenant"""
    policy_universe = modir.lookupByDn('uni')
    fvTenant = Tenant(policy_universe, tenant_name)

    # print the query in XML format
    print_query_xml(policy_universe)

    # Commit the change using a ConfigRequest object
    commit_change(modir, policy_universe)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
    else:
        hostname, username, password, tenant_name = sys.argv[1:]
    modir = apic_login(hostname, username, password)
    create_tenant(modir, tenant_name)
    modir.logout()
