from utility import *


def create_tenant(modir, tenant_name):
    """Create a tenant"""
    policy_universe = modir.lookupByDn('uni')
    fvTenant = Tenant(policy_universe, tenant_name)

    # print the query in XML format
    print_query_xml(policy_universe)

    # Commit the change using a ConfigRequest object
    commit_change(modir, policy_universe)


if __name__ == '__main__':

    try:
        host_name, user_name, password, tenant_name = sys.argv[1:]
    except ValueError:
        try:
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            tenant_name = data['tenant']
        except (IOError, KeyError, TypeError):
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()

    modir = apic_login(host_name, user_name, password)
    create_tenant(modir, tenant_name)
    modir.logout()
