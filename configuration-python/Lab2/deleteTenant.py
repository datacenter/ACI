from cobra.model.fv import Tenant

from utility import *


def delete_tenant(modir, tenant_name):
    """Delete a tenant"""
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)
    if isinstance(fv_tenant, Tenant):
        fv_tenant.delete()
    else:
        print 'Tenant', tenant_name, 'does not existed.'
        return

    # print the query in XML format
    print_query_xml(fv_tenant)

    # Commit the change using a ConfigRequest object
    commit_change(modir, fv_tenant)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
    else:
        hostname, username, password, tenant_name = sys.argv[1:]
    modir = apic_login(hostname, username, password)
    delete_tenant(modir, tenant_name)
    modir.logout()
