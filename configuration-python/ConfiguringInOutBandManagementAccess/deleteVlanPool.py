from cobra.model.fvns import VlanInstP, EncapBlk
from createVlanPool import input_key_args

from utility import *


key_args = [{'name': 'vlan_name', 'help': 'VLAN Pool name'},
            {'name': 'allocation_mode', 'help': 'Allocation Mode', 'choices': ['dynamic', 'static']}
            ]


def delete_vlan_pool(modir, vlan_name, allocation_mode):

    # Query to the VLAN pool.
    fvns_vlaninstp = modir.lookupByDn('uni/infra/vlanns-' + vlan_name + '-' + allocation_mode)

    if isinstance(fvns_vlaninstp, VlanInstP):
        # delete the VLAN
        fvns_vlaninstp.delete()
    else:
        print 'There is no VLAN', vlan_name, '(', allocation_mode, ').'
        return

    print_query_xml(fvns_vlaninstp)
    commit_change(modir, fvns_vlaninstp)


if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Delete VLAN Pool.', key_args)

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            vlan_name = data['vlan_name']
            allocation_mode = data['allocation_mode']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            vlan_name, allocation_mode = input_key_args(from_delete_function=True)

    else:
        vlan_name = args.pop('vlan_name')
        allocation_mode = args.pop('allocation_mode')

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_vlan_pool(modir, vlan_name, allocation_mode.lower())

    modir.logout()


