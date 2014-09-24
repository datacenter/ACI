from cobra.model.aaa import User, UserDomain, UserRole

from utility import *


key_args = [{'name': 'local_user', 'help': 'Name of the New Local User.'},
            {'name': 'security_domain', 'help': 'The Security Domain being added to.'}
]


def input_key_args(msg='\nPlease input User and Security Domain info:'):
    print msg
    args = []
    args.append(get_raw_input("User Name (required): ", required=True))
    args.append(get_raw_input("Security Domain Name (required): ", required=True))
    return args


def input_roles(msg='User Roles that to be added'):
    print msg
    return {'name':get_raw_input("Role Name (required): ", required=True),
            'type':get_optional_input("Role Type (required): ", ['readPriv(r)', 'writePriv(w)'], required=True)}


def add_user_role(modir, user, security_domain, roles, commit=True):

    def add_roles(parent, roles):
        for role in roles:
            aaa_role = UserRole(parent, role['name'],
                                privType=get_value(role, 'type', 'readPriv'))

    if isinstance(modir, UserDomain):
        aaa_domain = modir
        add_roles(aaa_domain, roles)

    else:
        # Query a User
        aaa_user = modir.lookupByDn('uni/userext/user-'+user)

        if isinstance(aaa_user, User):
            aaa_domain = modir.lookupByDn('uni/userext/user-'+user+'/userdomain-'+security_domain)

            if not isinstance(aaa_domain, UserDomain):

                print 'Security Domain', security_domain, 'does not existed. Creating one.'
                aaa_domain = UserDomain(aaa_user, security_domain)

            add_roles(aaa_domain, roles)

        else:
            print 'User', user, 'does not existed.'
            return

    if commit:
        print_query_xml(aaa_domain)
        commit_change(modir, aaa_domain)


if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        parser = set_cli_argparse('Add User Role to Security Domain.', key_args, return_parser=True)
        parser.add_argument('-r', '--read_priv_roles', dest='read_roles', nargs="*", help='Read Priv User Roles')
        parser.add_argument('-w', '--write_priv_roles', dest='write_roles', nargs="*", help='Write Priv User Roles')
        args = vars(parser.parse_args())

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            local_user = data['local_user']
            security_domain = data['security_domain']
            roles = data['roles']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            local_user, security_domain = input_key_args()
            roles = add_mos(input_roles, 'Add a User Role')

    else:
        host_name = args.pop('host')
        user_name = args.pop('user')
        password = args.pop('password')
        local_user = args.pop('local_user')
        security_domain = args.pop('security_domain')
        roles = []
        for role in args['read_roles']:
            roles.append({'name': role, 'type':'readPriv'})
        for role in args['write_roles']:
            roles.append({'name': role, 'type':'writePriv'})

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    add_user_role(modir, local_user, security_domain, roles)

    modir.logout()


