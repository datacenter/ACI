from cobra.model.fv import BD, RsBDToOut

from utility import *


def input_key_args(msg='Please input Bridge Domain and Network info:'):
    print msg
    args = []
    args.append(get_raw_input("Bridge Domain Name (required): ", required=True))
    args.append(get_raw_input("L3 Outside Network Name (required): ", required=True))
    return args


def disassociate_l3_outside_network_to_bd(modir, tenant_name, bridge_domain, routed_outside_name):

    fv_bd = modir.lookupByDn('uni/tn-' + tenant_name + '/BD-' + bridge_domain)
    if isinstance(fv_bd, BD):
        fv_rsbdtoout = modir.lookupByDn('uni/tn-' + tenant_name + '/BD-' + bridge_domain + '/rsBDToOut-' + routed_outside_name)
        if isinstance(fv_rsbdtoout, RsBDToOut):
            fv_rsbdtoout.delete()
        else:
            print 'Network', routed_outside_name, 'is not associating to Bridge Domain', bridge_domain
            return
    else:
        print 'Bridge Domain', bridge_domain, 'does not existed.'
        return

    print_query_xml(fv_rsbdtoout)
    commit_change(modir, fv_rsbdtoout)


if __name__ == '__main__':
    # Obtain the arguments from CLI
    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'bridge_domain', 'help': 'Bridge Domain Name.'},
                    {'name': 'routed_outside', 'help': 'Routed Outside Network Name.'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Disassociate the L3 Outside Network from a Bridge Domain', key_args)
        tenant_name = args.pop('tenant')
        bridge_domain = args.pop('bridge_domain')
        routed_outside_name = args.pop('routed_outside')

    except SystemExit:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        bridge_domain, routed_outside_name = input_key_args()
    modir = apic_login(host_name, user_name, password)
    disassociate_l3_outside_network_to_bd(modir, tenant_name, bridge_domain, routed_outside_name)
    modir.logout()
