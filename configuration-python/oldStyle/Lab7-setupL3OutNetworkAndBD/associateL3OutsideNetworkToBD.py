from cobra.model.fv import BD, RsBDToOut

from createRoutedOutside import input_key_args as input_L3_outside_network
from utility import *


def input_key_args(msg='Please input Bridge Domain and Network info:'):
    print msg
    return get_raw_input("Bridge Domain Name (required): ", required=True)


def associate_l3_outside_network_to_bd(modir, tenant_name, bridge_domain, routed_outside_name):
    fv_bd = modir.lookupByDn('uni/tn-' + tenant_name + '/BD-' + bridge_domain)
    if isinstance(fv_bd, BD):
        fv_rsbdtoout = RsBDToOut(fv_bd, routed_outside_name)
    else:
        print 'Bridge Domain', bridge_domain, 'does not existed.'
        return

    print_query_xml(fv_bd)
    commit_change(modir, fv_bd)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'bridge_domain', 'help': 'Bridge Domain Name.'},
                {'name': 'routed_outside', 'help': 'Routed Outside Network Name.'}
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Associate the L3 Outside Network to a Bridge Domain', key_args)
        tenant_name = args.pop('tenant')
        bridge_domain = args.pop('bridge_domain')
        routed_outside_name = args.pop('routed_outside')

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        bridge_domain = input_key_args()
        routed_outside_name = input_L3_outside_network()
    modir = apic_login(host_name, user_name, password)
    associate_l3_outside_network_to_bd(modir, tenant_name, bridge_domain, routed_outside_name)
    modir.logout()
