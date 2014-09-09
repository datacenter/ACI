from cobra.model.infra import AccPortGrp
from createAccessPortPolicyGroup import input_key_args

from utility import *

key_args = [{'name': 'group_name', 'help': 'Port Policy Group name'}]


def delete_access_port_port_policy_group(modir, group_name):

    # Query a parent
    infra_accportgrp = modir.lookupByDn('uni/infra/funcprof/accportgrp-'+group_name)
    if isinstance(infra_accportgrp, AccPortGrp):
        # delete the Access Port Policy Group
        infra_accportgrp.delete()
    else:
        print 'There is no Access Port Policy Group', group_name, '.'
        return

    print_query_xml(infra_accportgrp)
    commit_change(modir, infra_accportgrp)


if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('create Access Port Policy Group.', key_args)

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            group_name = data['group_name']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            group_name = input_key_args()

    else:
        group_name = args.pop('group_name')

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_access_port_port_policy_group(modir, group_name)

    modir.logout()
