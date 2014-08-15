import sys
from setAutonomousSystemNumber import set_autonomous_system_number
from createBgpRouteReflector import create_bgp_route_reflector
from createPodPolicyGroup import create_pod_policy_group, input_key_args
from selectPodPolicy import set_pod_selector

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
    set_pod_selector(modir, pod_policy)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        hostname, username, password = input_login_info()
        pod_policy = input_key_args()
    else:
        hostname, username, password, pod_policy = sys.argv[1:]
    modir = apic_login(hostname, username, password)
    lab7A(modir, pod_policy)
    modir.logout()
