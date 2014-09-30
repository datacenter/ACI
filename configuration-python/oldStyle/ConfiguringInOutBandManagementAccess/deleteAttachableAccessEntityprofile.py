from cobra.model.infra import AttEntityP

from createAttachableAccessEntityprofile import input_key_args
from utility import *


DEFAULT_ENABLE_INFRASTRUCTURE_VLAN = False

key_args = [{'name': 'profile_name', 'help': 'Attachable Access Entity Profile name'}]


def delete_attachable_access_entity_profile(modir, profile_name):

    # Query a parent
    infra_attentityp = modir.lookupByDn('uni/infra/attentp-'+profile_name)

    if isinstance(infra_attentityp, AttEntityP):
        # delete the Attachable Access Entity Profile
        infra_attentityp.delete()
    else:
        print 'There is no Attachable Access Entity Profile', profile_name, '.'
        return

    print_query_xml(infra_attentityp)
    commit_change(modir, infra_attentityp)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Delete Attachable Access Entity Profile.', key_args)

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
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

    else:
        profile_name = args.pop('profile_name')

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_attachable_access_entity_profile(modir, profile_name)

    modir.logout()
