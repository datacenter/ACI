from createRoutedOutside import input_key_args as input_routed_outside_name
from cobra.model.l3ext import Out, LNodeP

from utility import *


def input_key_args(msg='\nPlease input the Node Profile info'):
    print msg
    return get_raw_input("Node Profile Name (required): ", required=True)


def input_optional_args(*arg):
    args = {}
    args['targetDscp'] = get_optional_input('Target DSCP (default: "unspecified"): ', [], num_accept=True)
    return args


def create_node_profile(modir, tenant_name, routed_outside_name, node_profile_name, **args):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    l3ext_out = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name)
    if isinstance(l3ext_out, Out):
        l3ext_lnodep = LNodeP(l3ext_out, node_profile_name,
                              targetDscp=get_value(args, 'targetDscp', 'unspecified'))
    else:
        print 'External Routed Network', routed_outside_name, 'does not existed.'
    print_query_xml(l3ext_out)
    commit_change(modir, l3ext_out)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'routed_outside', 'help': 'Routed Outside Network Name.'},
                    {'name': 'node_profile', 'help': 'Node Profile Name.'}
        ]
        opt_args = [{'flag': 'D', 'name': 'targetDscp', 'help': 'Node level Dscp value.'}]

        host_name, user_name, password, args = set_cli_argparse('Create Node Profile.', key_args, opt_args)
        tenant_name = args.pop('tenant')
        routed_outside_name = args.pop('routed_outside')
        node_profile_name = args.pop('node_profile')
        optional_args = args

    except: #?error

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        node_profile_name = input_key_args()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_node_profile(modir, tenant_name, routed_outside_name, node_profile_name, args_from_CLI=optional_args)

    modir.logout()


