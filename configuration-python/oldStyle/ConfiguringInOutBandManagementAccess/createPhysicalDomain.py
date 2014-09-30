from cobra.model.phys import DomP
from cobra.model.infra import RsVlanNs

from utility import *


DEFAULT_VLAN_POOL = ''

key_args = [{'name': 'physical_domain', 'help': 'Physical Domain name'}]


opt_args = [{'flag': 'v', 'name': 'vlan_pool', 'help': 'VLAN Pool.'},
            {'flag': 'm', 'name': 'vlan_mode', 'help': 'VLAN Mode: Static/Dynamic', 'choices': ['dynamic', 'static']},
    ]


def input_key_args(msg='\nPlease specify the Physical Domain:'):
    print msg
    return get_raw_input("Physical Domain Name (required): ", required=True)


def input_optional_args():
    args = {}
    args['vlan_pool'] = get_raw_input('Vlan Name (default: None): ')
    if args['vlan_pool'] not in ['None', 'none', 'NONE', '']:
        args['vlan_mode'] = get_optional_input("Vlan Mode (required) ", ['dynamic(d)', 'static(s)'], required=True)
    return args


def create_physical_domain(modir, physical_domain, **args):

    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    # Query a parent
    uni = modir.lookupByDn('uni/')
    phys_domp = DomP(uni, physical_domain)

    if 'vlan_pool' in args.keys() and 'vlan_mode' in args.keys():
        infra_rsvlanns = RsVlanNs(phys_domp, tDn='uni/infra/vlanns-[' + args['vlan_pool'] + ']-' + args['vlan_mode'])
    print_query_xml(uni)
    commit_change(modir, uni)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Create Physical Domain.', key_args, opt_args)

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv, opt_args):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            physical_domain = data['physical_domain']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            physical_domain = input_key_args()
            optional_args = input_optional_args()
        else:
            if 'optional_args' in data.keys():
                optional_args = data['optional_args']
            else:
                optional_args = {}
    else:
        physical_domain = args.pop('physical_domain')
        optional_args = args

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_physical_domain(modir, physical_domain, args_from_CLI=optional_args)

    modir.logout()
