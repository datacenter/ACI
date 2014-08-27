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
    try:
        key_args = [{'name': 'spine', 'help': 'Spine ID'}]
        host_name, user_name, password, args = set_cli_argparse('Create a Bgp Route Reflector.', key_args)
        spine_id = args.pop('spine')

    except SystemExit:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        spine_id = input_key_args()


    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_bgp_route_reflector(modir, spine_id)

    modir.logout()


