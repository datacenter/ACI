from utility import *
from cobra.model.aaa import DomainRef


def input_key_args(msg='Please input Security Domain info:'):
    print msg
    return get_raw_input("Security Domain Name (required): ", required=True)


def add_security_domain(modir, tenant_name, security_domain):
    """Add security domain to tenant"""
    # query the tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)
    aaa_domain_ref = DomainRef(fv_tenant, security_domain)

    # print out in XML format
    print_query_xml(fv_tenant)
    # summit change.
    commit_change(modir, fv_tenant)


if __name__ == '__main__':
    
    if len(sys.argv) == 6:
        host_name, user_name, password, tenant_name, security_domain = sys.argv[1:]
    else:
        try:
            data = read_config_yaml_file(sys.argv[1])            
            host_name = data['host_name']
            user_name = data['user_name']
            password = data['password']
            tenant_name = data['tenant_name']
            security_domain = data['security_domain']
        except (IOError, KeyError, TypeError):
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            security_domain = input_key_args()


    modir = apic_login(host_name, user_name, password)
    add_security_domain(modir, tenant_name, security_domain)
    modir.logout()
