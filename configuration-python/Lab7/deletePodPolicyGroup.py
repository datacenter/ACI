from createPodPolicyGroup import input_key_args, PodPGrp
from utility import *


def delete_pod_policy_group(modir, policy_name):

    # Query to the Route Reflector Node.
    fabric_podpgrp = modir.lookupByDn('uni/fabric/funcprof/podpgrp-' + policy_name)

    if isinstance(fabric_podpgrp, PodPGrp):
        fabric_podpgrp.delete()
    else:
        print 'Pod group policy', policy_name, 'is not existed.'
        return

    print_query_xml(fabric_podpgrp)
    commit_change(modir, fabric_podpgrp)

if __name__ == '__main__':

    # Obtain the key parameters.
    key_args = [{'name': 'policy_group', 'help': 'Policy Group name'}]
    try:
        host_name, user_name, password, args = set_cli_argparse('Delete a Pod Policy Group.', key_args)
        policy_group_name = args.pop('policy_group')
        optional_args = args

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        policy_group_name = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_pod_policy_group(modir, policy_group_name)

    modir.logout()


