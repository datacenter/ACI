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

    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'bridge_domain', 'help': 'Bridge Domain'},
                ]
    try:
        host_name, user_name, password, args = set_cli_argparse('Delete a Bridge Domain.', key_args)
        tenant_name = args.pop('tenant')
        bridge_domain = args.pop('bridge_domain')

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            tenant_name = data['tenant']
            bridge_domain = data['bridge_domain']['name']
        except (IOError, KeyError, TypeError, IndexError):
            if len(sys.argv)>1:
                print 'Invalid input arguments.'
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            bridge_domain = input_key_args()

    modir = apic_login(host_name, user_name, password)
    delete_bridge_domain(modir, tenant_name, bridge_domain)
    modir.logout()
