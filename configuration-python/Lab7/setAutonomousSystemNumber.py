import sys
from cobra.model.bgp import AsP

from utility import *


def input_key_args(msg='\nPlease set Autonomous System Number:'):
    print msg
    return get_optional_input("Number (required) ", [], num_accept=True)


def set_autonomous_system_number(modir, autonomous_system_number):

    bgp_instpol = modir.lookupByDn('uni/fabric/bgpInstP-default')
    # Set Autonomous System Number
    bgp_asp = AsP(bgp_instpol, asn=autonomous_system_number)

    print toXMLStr(bgp_instpol, prettyPrint=True)
    commit_change(modir, bgp_instpol)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        host_name, user_name, password, autonomous_system_number = sys.argv[1:5]
    except ValueError:
        host_name, user_name, password = input_login_info()
        autonomous_system_number = input_key_args()


    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    set_autonomous_system_number(modir, autonomous_system_number)

    modir.logout()


