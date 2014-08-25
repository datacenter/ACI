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
    delete_tenant(modir, tenant_name)
    modir.logout()
