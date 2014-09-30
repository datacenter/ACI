from cobra.model.bgp import AsP

from utility import *


def reset_autonomous_system_number(modir):

    bgp_asp = modir.lookupByDn('uni/fabric/bgpInstP-default/as')
    # Set Autonomous System Number
    if isinstance(bgp_asp, AsP):
        bgp_asp.delete()
    else:
        print 'Autonomous System Number has not been set.'

    print_query_xml(bgp_asp)
    commit_change(modir, bgp_asp)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        host_name, user_name, password, args = set_cli_argparse('Reset Autonomous System Number.', [])

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    reset_autonomous_system_number(modir)

    modir.logout()


