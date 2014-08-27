from createRoutedOutside import input_key_args
from cobra.model.l3ext import Out

from utility import *


def delete_routed_outside(modir, tenant_name, routed_outside_name):
    l3ext_out = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name)
    if isinstance(l3ext_out, Out):
        l3ext_out.delete()
    else:
        print 'External Routed Network', routed_outside_name, 'does not existed.'
        return
    print_query_xml(l3ext_out)
    commit_change(modir, l3ext_out)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'routed_outside', 'help': 'Routed Outside Network Name.'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Delete a Routed Outside Network.', key_args)
        tenant_name = args.pop('tenant')
        routed_outside_name = args.pop('routed_outside')

    except SystemExit:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_routed_outside(modir, tenant_name, routed_outside_name)

    modir.logout()


