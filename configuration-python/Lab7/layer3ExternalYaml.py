from utility import *
from setAutonomousSystemNumber import set_autonomous_system_number
from createBgpRouteReflector import create_bgp_route_reflector
from createPodPolicyGroup import create_pod_policy_group
from selectPodPolicy import select_pod_policy


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Configure fabric pod policy.')
    parser.add_argument('yaml', help='Imported yaml file.')
    args = vars(parser.parse_args())

    try:
        data = read_config_yaml_file(args['yaml'], login_info=False)
    except IOError:
        print 'No such file or directory:', args['yaml']
        sys.exit()
    else:
        host, user, password = get_login_info(data)
        modir = apic_login(host, user, password)


    # Set Autonomous System Number
    set_autonomous_system_number(modir, data['autonomous_system_number'])

    # Create BGP Route Reflector
    for reflector in data['reflector_id']:
        create_bgp_route_reflector(modir, reflector)

    # Create Policy Group
    for group in data['pod_policy_group']:
        create_pod_policy_group(modir, group['name'],
                                tnBgpInstPolName=group[
                                    'bgp_route_reflector_policy'],
                                tnIsisDomPolName=group['isis_policy'],
                                tnCoopPolName=group['coop_group_policy'],
                                tnDatetimePolName=group['date_time_policy'],
                                tnCommPolName=group['communication_policy'],
                                tnSnmpPolName=group['snmp_policy'])

    # Select Fabric Policy Group
    select_pod_policy(modir, data['selected_pod_policy_group'])

