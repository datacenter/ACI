from cobra.model.bgp import RRNodePEp

from utility import *


def input_key_args(msg='\nPlease input BGP Route Reflector info:'):
    print msg
    return get_raw_input("Spine ID (required): ", required=True)


def create_bgp_route_reflector(modir, spine_id):

    bgp_rrp = modir.lookupByDn('uni/fabric/bgpInstP-default/rr')
    # create Route Reflector Node
    bgp_rrnodepep = RRNodePEp(bgp_rrp, spine_id)

    print_query_xml(bgp_rrp)
    commit_change(modir, bgp_rrp)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        host_name, user_name, password, spine_id = sys.argv[1:5]
    except ValueError:
        host_name, user_name, password = input_login_info()
        spine_id = input_key_args()


    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_bgp_route_reflector(modir, spine_id)

    modir.logout()


