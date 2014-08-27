from utility import *
from cobra.model.aaa import DomainRef


def input_key_args(msg='Please input Security Domain info:'):
    print msg
    return get_raw_input("Security Domain Name (required): ", required=True)


def add_security_domain(modir, tenant_name, security_domain):
    """Add security domain to tenant"""
    # query the tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)

    def add_a_security_domain(sd):
        aaa_domain_ref = DomainRef(fv_tenant, sd)

    if type(security_domain) == list:
        for sd in security_domain:
            add_a_security_domain(sd)
    else:
        add_a_security_domain(security_domain)

    # print out in XML format
    print_query_xml(fv_tenant)
    # summit change.
    commit_change(modir, fv_tenant)


if __name__ == '__main__':
    
    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'security_domain', 'help': 'Security Domain Name'}]
        host_name, user_name, password, args = set_cli_argparse('Create a Security Domain.', key_args)
        tenant_name = args.pop('tenant')
        security_domain = args.pop('security_domain')

    except:

        if sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        try:
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            tenant_name = data['tenant']
            security_domain = data['security_domain']
        except (IOError, KeyError, TypeError):
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            security_domain = input_key_args()


    modir = apic_login(host_name, user_name, password)
    add_security_domain(modir, tenant_name, security_domain)
    modir.logout()
