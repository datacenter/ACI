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

    # Obtain the arguments from CLI
    key_args = [{'name': 'tenant', 'help': 'Tenant name'}]
    try:
        host_name, user_name, password, args = set_cli_argparse('Create a plain tenant.', key_args)
        tenant_name = args.pop('tenant')

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            tenant_name = data['tenant']
        except (IOError, KeyError, TypeError, IndexError):
            if len(sys.argv)>1:
                print 'Invalid input arguments.'
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()

    modir = apic_login(host_name, user_name, password)
    create_tenant(modir, tenant_name)
    modir.logout()
