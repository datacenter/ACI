from createFilter import input_key_args, Filter
from utility import *


def delete_filter(modir, tenant_name, filter_name):
    # Check if the filter exists or not. If yes, delete it.
    fv_ct = modir.lookupByDn('uni/tn-' + tenant_name + '/flt-' + filter_name)
    if isinstance(fv_ct, Filter):
        fv_ct.delete()
    else:
        print 'There is no filter called', filter_name, 'in tenant', tenant_name, '.'
        return

    print_query_xml(fv_ct)

    commit_change(modir, fv_ct)


if __name__ == '__main__':

    try:
        host_name, user_name, password, tenant_name, filter_name = sys.argv[1:]
    except ValueError:
        try:
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            tenant_name = data['tenant']
            filter_name = data['filter']
            optional_args = data['optional_args']
        except (IOError, KeyError, TypeError):
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            filter_name = input_key_args()

    modir = apic_login(host_name, user_name, password)
    delete_filter(modir, tenant_name, filter_name)
    modir.logout()
