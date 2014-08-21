from cobra.model.fvns import VlanInstP
from createVlanPool import input_key_args

from utility import *


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

    # Obtain the key parameters.
    try:
        host_name, user_name, password, vlan_name, allocation_mode = sys.argv[1:6]
    except ValueError:
        host_name, user_name, password = input_login_info()
        vlan_name, allocation_mode, vlan_range_from, vlan_range_to = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if allocation_mode.lower() not in ['dynamic', 'static']:
        print 'VM provider has to be either be \"dynamic\" or \"static\"'
    else:
        delete_vlan_pool(modir, vlan_name, allocation_mode.lower())

    modir.logout()


