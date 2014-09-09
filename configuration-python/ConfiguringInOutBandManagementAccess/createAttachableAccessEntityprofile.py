from cobra.model.infra import AttEntityP, RsDomP, ProvAcc

from utility import *

DEFAULT_ENABLE_INFRASTRUCTURE_VLAN = False

key_args = [{'name': 'profile_name', 'help': 'Attachable Access Entity Profile name'}]


opt_args = [{'flag': 'v', 'name': 'enable_infrastructure_vlan', 'help': 'Enable Infrastructure VLAN.', 'choices': ['True', 'False']},
    ]


def input_key_args(msg='\nPlease specify the Attachable Access Entity Profile:'):
    print msg
    return get_raw_input("Entity Profile Name (required): ", required=True)


def input_domain_name():
    return get_raw_input('Domain name (required): ', required=True)


def input_optional_args():
    args = {}
    args['enable_infrastructure_vlan'] = get_optional_input('Enable Infrastructure VLAN? (Default: '+str(DEFAULT_ENABLE_INFRASTRUCTURE_VLAN)+'): ', ['True(T)', 'False(F)'])
    args['domain_profiles'] = add_mos(input_domain_name, 'Add a Domain Profile')
    return args


def create_attachable_access_entity_profile(modir, profile_name, **args):

    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    # Query a parent
    infra = modir.lookupByDn('uni/infra')
    infra_attentityp = AttEntityP(infra, profile_name)

    if 'enable_infrastructure_vlan' in args.keys():
        if args['enable_infrastructure_vlan'] in [True, 'True']:
            infra_provacc = ProvAcc(infra_attentityp)
        elif args['enable_infrastructure_vlan'] in [False, 'False']:
            infra_provacc = ProvAcc(infra_attentityp)
            infra_provacc.delete()


    if 'domain_profiles' in args.keys():
        for domain in args['domain_profiles']:
            infra_rsdomp = RsDomP(infra_attentityp, 'uni/phys-'+domain)
    print_query_xml(infra)
    commit_change(modir, infra)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        parser = set_cli_argparse('Create Attachable Access Entity Profile.', key_args, opt_args, return_parser=True)
        parser.add_argument('-d', '--domains', dest='domain_profiles', nargs="*", help='The security domains')
        args = vars(parser.parse_args())


    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv, opt_args):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            profile_name = data['profile_name']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            profile_name = input_key_args()
            optional_args = input_optional_args()

        else:
            if 'optional_args' in data.keys():
                optional_args = data['optional_args']
            else:
                optional_args = {}
    else:
        host_name = args.pop('host')
        user_name = args.pop('user')
        password = args.pop('password')
        profile_name = args.pop('profile_name')
        optional_args = args

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_attachable_access_entity_profile(modir, profile_name, args_from_CLI=optional_args)

    modir.logout()
