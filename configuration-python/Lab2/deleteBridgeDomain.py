from cobra.model.fv import BD

from utility import *


def input_key_args(msg='Please input Bridge Domain info:'):
    print msg
    return get_raw_input("Bridge Domain Name (required): ", required=True)


def delete_bridge_domain(modir, tenant_name, bridge_domain):
    """Delete a bridge domain"""
    fv_bd = modir.lookupByDn('uni/tn-' + tenant_name + '/BD-' + bridge_domain)
    if isinstance(fv_bd, BD):
        fv_bd.delete()
    else:
        print 'Bridge Domain', bridge_domain, 'does not existed.'
        return

    print_query_xml(fv_bd)
    commit_change(modir, fv_bd)

if __name__ == '__main__':
    if len(sys.argv) == 6:
        host_name, user_name, password, tenant_name, bridge_domain = sys.argv[1:]
    else:
        try:
            data = read_config_yaml_file(sys.argv[1])
            host_name = data['host_name']
            user_name = data['user_name']
            password = data['password']
            tenant_name = data['tenant_name']
            bridge_domain = data['bridge_domain']['name']
        except (IOError, KeyError, TypeError):
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            bridge_domain = input_key_args()

        host_name, user_name, password, tenant_name, bridge_domain = sys.argv[1:]
    modir = apic_login(host_name, user_name, password)
    delete_bridge_domain(modir, tenant_name, bridge_domain)
    modir.logout()
