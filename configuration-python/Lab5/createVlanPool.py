from cobra.model.fvns import VlanInstP, EncapBlk

from utility import *


def input_key_args(msg='\nPlease input Vlan pool info:'):
    print msg
    args = []
    args.append(get_raw_input("Name (required): ", required=True))
    args.append(get_optional_input("Allocation Mode (required) ", ['dynamic(d)', 'static(s)'], required=True))
    args.append(get_raw_input("Vlan Range From (required): ", required=True))
    args.append(get_raw_input("Vlan Range To (required): ", required=True))
    print args
    return args


def create_vlan_pool(modir, vlan_name, allocation_mode, vlan_range_from, vlan_range_to):

    # Query to the vlan pool collections.
    infra_infra = modir.lookupByDn('uni/infra')
    # Create a VLAN.
    fvns_vlaninstp = VlanInstP(infra_infra, vlan_name, allocation_mode)
    # Set up the VLAN range.
    fvns_encapblk = EncapBlk(fvns_vlaninstp, 'vlan-'+vlan_range_from, 'vlan-'+vlan_range_to)
    print_query_xml(infra_infra)
    commit_change(modir, infra_infra)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        host_name, user_name, password, vlan_name, allocation_mode, vlan_range_from, vlan_range_to = sys.argv[1:8]
    except ValueError:
        host_name, user_name, password = input_login_info()
        vlan_name, allocation_mode, vlan_range_from, vlan_range_to = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if allocation_mode.lower() not in ['dynamic', 'static']:
        print 'VM provider has to be either be \"dynamic\" or \"static\"'
    else:
        create_vlan_pool(modir, vlan_name, allocation_mode.lower(), vlan_range_from, vlan_range_to)

    modir.logout()


