from cobra.model.aaa import User
from utility import *

DEFAULT_XXXX = 'unspecified'


def input_key_args(msg='\nPlease input XXXX info:'):
    print msg
    return get_raw_input("XXXX Name (required): ", required=True)


def input_optional_args():
    args = {}
    args['xxx_name'], = get_raw_input('xxx Name (default: "' + DEFAULT_XXXX + '"): '),
    return args


def create_XXXX(modir, *keyargs, **args):

    # Query a parent
    xx_parent = modir.lookupByDn('uni/tn-' + parent)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args

    # Check if the parent exists
    if isinstance(xx_parent, Parent):
        # Create a MO
        xx_mo = MO(xx_parent, mo)

    else:
        print 'Parent', parent, 'does not exist. Please create a parent first'
        return

    print_query_xml(xx_parent)
    commit_change(modir, xx_parent)

if __name__ == '__main__':

    # Obtain the arguments from CLI
    key_args = [{'name': 'parent', 'help': 'Parent name'},
                {'name': 'mo', 'help': 'MO name'}
    ]
    opt_args = [{'flag': 'a', 'name': 'aaa', 'default': DEFAULT_, 'help': 'aaa is '},
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Create a MO.', key_args, opt_args)
        key_args = args.pop('')
        optional_args = args

    except SystemExit:

        if check_if_requesting_help(sys.argv, opt_args):
            sys.exit('Help Page')

        try:
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            key_args = data['key_args']
            optional_args = data['optional_args']
        except (IOError, KeyError, TypeError, IndexError):
            if len(sys.argv)>1:
                print 'Invalid input arguments.'
            host_name, user_name, password = input_login_info()
            key_args = input_key_args()
            optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_XXXX(modir, key_args, args_from_CLI=optional_args)

    modir.logout()


