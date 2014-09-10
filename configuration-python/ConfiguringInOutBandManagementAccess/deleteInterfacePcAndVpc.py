from cobra.model.infra import AccPortP, NodeP
from configureInterfacePcAndVpc import input_key_args
from utility import *

DEFAULT_INTERFACE_TYPE = 'individual'
DEFAULT_TYPE = 'range'

key_args = [{'name': 'switch_profile', 'help': 'Switch Profile Name'}]


def delete_interface_pc_and_vpc(modir, switch_profile):

    # Query a parent
    infra_accportp = modir.lookupByDn('uni/infra/accportprof-'+switch_profile+'_ifselector')
    infra_nodep = modir.lookupByDn('uni/infra/nprof-'+switch_profile)

    if isinstance(infra_accportp, AccPortP):
        infra_accportp.delete()
    else:
        print 'Interface Profile'+ switch_profile+'_ifselector does not exist.'

    if isinstance(infra_nodep, NodeP):
        infra_nodep.delete()
    else:
        print 'Switch Profile'+ switch_profile+' does not exist.'

    print_query_xml(infra_accportp)
    commit_change(modir, infra_accportp)

    print_query_xml(infra_nodep)
    commit_change(modir, infra_nodep)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Delete Interface PC and VPC.', key_args)

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            switch_profile = data['switch_profile']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            switch_profile = input_key_args()
    else:
        switch_profile = args.pop('switch_profile')

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_interface_pc_and_vpc(modir, switch_profile)

    modir.logout()
