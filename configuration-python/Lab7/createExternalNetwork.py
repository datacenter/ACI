from createRoutedOutside import input_key_args as input_routed_outside_name
from cobra.model.l3ext import InstP, Subnet

from utility import *

def input_key_args(msg='\nPlease input External EPG Network info'):
    print msg
    return get_raw_input("EPG Network Name (required): ", required=True)


def input_optional_args(*arg):
    args = {}
    args['prio'] = get_optional_input('QoS Class (default: "unspecified"): ', ['level1', 'level2', "level3", "unspecified"])
    args['subnet_ip'] = get_raw_input('Subnet IP Address (optional): ')
    return args


def create_external_network(modir, tenant_name, routed_outside_name, external_network_name, **args):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    l3ext_out = modir.lookupByDn('uni/tn-'+tenant_name+'/out-'+routed_outside_name)

    if l3ext_out is None:
        print 'External Routed Network', routed_outside_name, 'does not existed.'
        return

    l3ext_instp = InstP(l3ext_out, external_network_name,
                        prio=get_value(args,'prio', 'unspecified'))

    if 'subnet_ip' in args.keys() and args['subnet_ip'] != '':
        l3ext_subnet = Subnet(l3ext_instp, args['subnet_ip'])

    print_query_xml(l3ext_out)
    commit_change(modir, l3ext_out)

if __name__ == '__main__':

    # Obtain the arguments from CLI
    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'routed_outside', 'help': 'Routed Outside Network Name.'},
                    {'name': 'external_network', 'help': 'External Network Name.'},
        ]
        opt_args = [{'flag': 's', 'name': 'subnet', 'dest': 'subnet_ip', 'help': 'The network visibility of the domain. '},
                    {'flag': 'Q', 'name': 'QoS_class', 'dest': 'prio', 'help': 'The priority level of a sub application running behind an endpoint group.'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Create External Network EPG.', key_args, opt_args)
        tenant_name = args.pop('tenant')
        routed_outside_name = args.pop('routed_outside')
        external_network_name = args.pop('external_network')
        optional_args = args

    except EOFError: #?error

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        external_network_name = input_key_args()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_external_network(modir, tenant_name, routed_outside_name, external_network_name, args_from_CLI=optional_args)

    modir.logout()


