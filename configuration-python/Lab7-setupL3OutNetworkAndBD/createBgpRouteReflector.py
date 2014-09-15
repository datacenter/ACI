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

    # Obtain the arguments from CLI
    key_args = [{'name': 'spine', 'help': 'Spine ID'}]
    try:
        host_name, user_name, password, args = set_cli_argparse('Create a Bgp Route Reflector.', key_args)
        spine_id = args.pop('spine')

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        spine_id = input_key_args()


    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_bgp_route_reflector(modir, spine_id)

    modir.logout()


