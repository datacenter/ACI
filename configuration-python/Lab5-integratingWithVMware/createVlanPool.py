from cobra.model.fvns import VlanInstP, EncapBlk

from utility import *


key_args = [{'name': 'vlan_name', 'help': 'VLAN Pool name'},
            {'name': 'allocation_mode', 'help': 'Allocation Mode', 'choices': ['dynamic', 'static']},
            {'name': 'range_from', 'help': 'VLAN range from'},
            {'name': 'range_to', 'help': 'VLAN range to'},
            ]


def input_key_args(msg='\nPlease specify the VLAN Pool identity:', from_delete_function=False):
    print msg
    args = []
    args.append(get_raw_input("VLan Name (required): ", required=True))
    args.append(get_optional_input("Allocation Mode (required) ", ['dynamic(d)', 'static(s)'], required=True))
    if not from_delete_function:
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

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Create VLAN Pool.', key_args)

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            vlan_name = data['vlan_name']
            allocation_mode = data['allocation_mode']
            range_from = data['range_from']
            range_to = data['range_to']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            vlan_name, allocation_mode, range_from, range_to = input_key_args()

    else:
        vlan_name = args.pop('vlan_name')
        allocation_mode = args.pop('allocation_mode')
        range_from = args.pop('range_from')
        range_to = args.pop('range_to')

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_vlan_pool(modir, vlan_name, allocation_mode.lower(), range_from, range_to)

    modir.logout()


