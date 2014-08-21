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
    if len(sys.argv) != 6:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
        security_domain = input_key_args()
    else:
        hostname, username, password, tenant_name, security_domain = sys.argv[1:]

    modir = apic_login(hostname, username, password)
    add_security_domain(modir, tenant_name, security_domain)
    modir.logout()
