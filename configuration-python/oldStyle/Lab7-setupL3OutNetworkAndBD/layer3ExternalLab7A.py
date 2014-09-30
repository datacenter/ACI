from setAutonomousSystemNumber import set_autonomous_system_number
from createBgpRouteReflector import create_bgp_route_reflector
from createPodPolicyGroup import create_pod_policy_group, input_key_args
from selectPodPolicy import select_pod_policy

from utility import *


def lab7A(modir, pod_policy):
    """Setup the Pod Policies"""

    # Set Autonomous System Number
    set_autonomous_system_number(modir, '1')
    # Create BGP Route Reflector
    create_bgp_route_reflector(modir, '103')
    create_bgp_route_reflector(modir, '104')
    # Create Policy Group
    create_pod_policy_group(modir, pod_policy, tnBgpInstPolName='default', tnIsisDomPolName='', tnCoopPolName='',
                            tnDatetimePolName='', tnCommPolName='', tnSnmpPolName='')
    # Select Fabric Policy Group
    select_pod_policy(modir, pod_policy)


if __name__ == '__main__':
    
    # Obtain the key parameters.
    key_args = [{'name': 'policy_group', 'help': 'Policy Group name'}]
    try:
        host_name, user_name, password, args = set_cli_argparse('Configure Fabric Pod Policy Group.', key_args)
        pod_policy = args.pop('policy_group')

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        pod_policy = input_key_args()
    modir = apic_login(host_name, user_name, password)
    lab7A(modir, pod_policy)
    modir.logout()
