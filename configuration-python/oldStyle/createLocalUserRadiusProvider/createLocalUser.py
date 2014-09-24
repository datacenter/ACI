from cobra.model.aaa import User, UserDomain

import addUserSecurityDomainAndRole as addRole
from utility import *


DEFAULT_STATUS = 'active'
DEFAULT_EXPIRES = 'no'

key_args = [{'name': 'local_user', 'help': 'Name of the New Local User'},
            {'name': 'local_password', 'help': 'Password of the New Local User'}
]

opt_args = [{'flag': 'f', 'name': 'first_name', 'help': 'User First Name.'},
            {'flag': 'l', 'name': 'last_name', 'help': 'User Last Name.'},
            {'flag': 'p', 'name': 'phone', 'help': 'User Phone Number'},
            {'flag': 'e', 'name': 'email', 'help': 'User Email'},
            {'flag': 'D', 'name': 'description', 'help': 'Description of the User'},
]


def input_security_domain(msg='\nPlease input Security Domain info:'):
    print msg
    return {'name': addRole.input_key_args(msg=''),
            'roles': add_mos(addRole.input_roles, 'Add a User Role')}


def input_key_args(msg='\nPlease input User info:', from_delete_function=False):
    print msg
    args = []
    args.append(get_raw_input("User Name (required): ", required=True))
    if not from_delete_function:
        args.append(get_raw_input("Password (required): ", required=True))
    return args


def input_optional_args():
    args = {}
    args['first_name'], = get_raw_input('User First Name (default: None): '),
    args['last_name'], = get_raw_input('User Last Name (default: None): '),
    args['phone'], = get_raw_input('User Phone Number (default: None): '),
    args['email'], = get_raw_input('User Email (default: None): '),
    args['description'], = get_raw_input('User Description (default: None): '),
    args['status'], = get_optional_input('Accout Status (default: "' + DEFAULT_STATUS + '")', ['inactive(i)', 'active(a)']),
    args['expires'], = get_optional_input('Account Status (default: "' + DEFAULT_EXPIRES + '")', ['yes(y)', 'no(n)']),
    if args['expires'] == 'yes':
        args['expiration_date'], = get_raw_input('The Date that Account Expires (Format: YYYY-MM-DD HH:MM:SS AM/PM): ', required=True),
    args['security_domain'] = add_mos(input_security_domain, 'Add a Security Domain')

    return args


def create_user(modir, local_user, local_password, **args):

    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    if get_value(args, 'expires', DEFAULT_EXPIRES) != 'yes':
        args['expiration_date'] = None
    # Query a parent
    aaa_userep = modir.lookupByDn('uni/userext')
    aaa_user = User(aaa_userep, local_user, pwd=local_password,
                    firstName=get_value(args, 'first_name', ''),
                    lastName=get_value(args, 'last_name', ''),
                    phone=get_value(args, 'phone', ''),
                    email=get_value(args, 'email', ''),
                    descr=get_value(args, 'description', ''),
                    accountStatus=get_value(args, 'status', DEFAULT_STATUS),
                    expires=get_value(args, 'expires', DEFAULT_EXPIRES),
                    expiration=get_value(args, 'expiration_date', '')
                    )

    if args['security_domain'] is not None:
        for sd in args['security_domain']:
            if type(sd) is dict:
                aaa_userdomain = UserDomain(aaa_user, sd['name'])
                addRole.add_user_role(aaa_userdomain, local_user, sd['name'], sd['roles'], commit=False)
            else:
                aaa_userdomain = UserDomain(aaa_user, sd)

    print_query_xml(aaa_userep)
    commit_change(modir, aaa_userep)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        parser = set_cli_argparse('Create a Local User.', key_args, opt_args, return_parser=True)
        parser.add_argument('-s', '--security_domain', dest='security_domain', nargs="*", help='The security domains')
        parser.add_argument('-S', '--status', help='Account Status', choices=['active', 'inactive']),
        parser.add_argument('-E', '--expires', help='Account Expires', choices=['yes', 'no']),
        parser.add_argument('-d', '--expiration_date', help='The Date that Account Expires'),
        args = vars(parser.parse_args())

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv, opt_args):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            local_user = data['local_user']
            local_password = data['local_password']
            optional_args = data['optional_args']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            local_user, local_password = input_key_args()
            optional_args = input_optional_args()

    else:
        host_name = args.pop('host')
        user_name = args.pop('user')
        password = args.pop('password')
        local_user = args.pop('local_user')
        local_password = args.pop('local_password')
        optional_args = args

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_user(modir, local_user, local_password, args_from_CLI=optional_args)

    modir.logout()


