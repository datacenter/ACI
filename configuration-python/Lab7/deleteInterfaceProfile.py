from cobra.model.l3ext import LIfP
from createRoutedOutside import input_key_args as input_routed_outside_name
from createNodesAndInterfacesProfile import input_key_args as input_node_profile_name
from createInterfaceProfile import input_key_args

from utility import *


def delete_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    l3ext_lifp = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name + '/lnodep-' + node_profile_name + '/lifp-' + interface_name)
    if isinstance(l3ext_lifp, LIfP):
        l3ext_lifp.delete()
    else:
        print 'Interface Profile', interface_name, 'does not existed.'
        return
    print_query_xml(l3ext_lifp)
    commit_change(modir, l3ext_lifp)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'routed_outside', 'help': 'Routed Outside Network Name.'},
                {'name': 'node_profile', 'help': 'Node Profile Name.'},
                {'name': 'interface_name', 'help': 'Interface Name.'}
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Delete interface profile.', key_args)
        tenant_name = args.pop('tenant')
        routed_outside_name = args.pop('routed_outside')
        node_profile_name = args.pop('node_profile')
        interface_name = args.pop('interface_name')

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        node_profile_name = input_node_profile_name()
        interface_name = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_interface_profile(modir, tenant_name, routed_outside_name, node_profile_name, interface_name)

    modir.logout()


