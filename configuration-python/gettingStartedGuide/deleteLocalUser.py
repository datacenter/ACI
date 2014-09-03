from cobra.model.aaa import User
from createLocalUser import input_key_args
from utility import *

key_args = [{'name': 'local_user', 'help': 'Name of the New Local User'},
]


def delete_user(modir, local_user):

    # Query a User
    aaa_user = modir.lookupByDn('uni/userext/user-'+local_user)

    if isinstance(aaa_user, User):
        aaa_user.delete()
    else:
        print 'User', local_user, 'does not existed.'
        return

    print_query_xml(aaa_user)
    commit_change(modir, aaa_user)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Delete a Local User.', key_args)

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            local_user = data['local_user']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            local_user = input_key_args(from_delete_function=True)[0]

    else:
        local_user = args.pop('local_user')

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_user(modir, local_user)

    modir.logout()


