import sys
from utility import *
import setAutonomousSystemNumber
import createBgpRouteReflector
import createPodPolicyGroup
import selectPodPolicy


if __name__ == '__main__':

    # Login
    hostname, username, password = '172.22.233.207', 'admin', 'Cisco123'  # input_login_info(msg='')
    try:
        modir = apic_login(hostname, username, password)
        print 'Login succeed.'
    except KeyError:
        print 'Login fail.'
        sys.exit()

    # Wizard starts asking inputs step by step
    autonomous_system_number = setAutonomousSystemNumber.input_key_args()
    bgp_route_reflector_array = add_mos(createBgpRouteReflector.input_key_args, 'Create a BGP Route Reflector')
    pod_policy_array = add_mos_with_options(createPodPolicyGroup.input_key_args, createPodPolicyGroup.input_optional_args, 'Create a Pod Policy')
    selected_pod_policy = selectPodPolicy.input_key_args()

    # Running
    setAutonomousSystemNumber.set_autonomous_system_number(modir, autonomous_system_number)
    for bgp_route_reflector in bgp_route_reflector_array:
        createBgpRouteReflector.create_bgp_route_reflector(modir, bgp_route_reflector)
    for pod_policy in pod_policy_array:
        print pod_policy
        createPodPolicyGroup.create_pod_policy_group(modir, pod_policy[0], args_from_CLI=pod_policy[1])
    selectPodPolicy.select_pod_policy(modir, selected_pod_policy)

    modir.logout()
