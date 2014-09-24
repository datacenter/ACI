from cobra.model.aaa import UserDomain

from addUserSecurityDomainAndRole import input_key_args
from utility import *


key_args = [{'name': 'local_user', 'help': 'Name of the New Local User.'},
            {'name': 'security_domain', 'help': 'The Security Domain being added to.'}
]


def delete_user_role(modir, user, security_domain):

    aaa_userDomain = modir.lookupByDn('uni/userext/user-'+user+ '/userdomain-'+security_domain)

    if isinstance(aaa_userDomain, UserDomain):
        aaa_userDomain.delete()

    else:
        print 'Security Domain', security_domain, 'does not existed.'
        return

    print_query_xml(aaa_userDomain)
    commit_change(modir, aaa_userDomain)


if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        parser = set_cli_argparse('Delete Security Domain.', key_args, return_parser=True)
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
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = '172.22.233.207','admin','Cisco123'#input_login_info()
            local_user, security_domain = input_key_args()

    else:
        host_name = args.pop('host')
        user_name = args.pop('user')
        password = args.pop('password')
        local_user = args.pop('local_user')
        security_domain = args.pop('security_domain')

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_user_role(modir, local_user, security_domain)

    modir.logout()


