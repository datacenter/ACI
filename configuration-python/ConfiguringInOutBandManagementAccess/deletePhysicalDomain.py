from cobra.model.phys import DomP
from cobra.model.infra import RsVlanNs

from createPhysicalDomain import input_key_args
from utility import *

DEFAULT_VLAN_POOL = ''

key_args = [{'name': 'physical_domain', 'help': 'Physical Domain name'}]


def delete_physical_domain(modir, physical_domain):

    # Query the physical domain
    phys_domp = modir.lookupByDn('uni/phys-'+physical_domain)
    if isinstance(phys_domp, DomP):
        # delete the Physical Domain
        phys_domp.delete()
    else:
        print 'There is no Physical Domain', physical_domain, '.'
        return

    print_query_xml(phys_domp)
    commit_change(modir, phys_domp)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Create Physical Domain.', key_args)

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            physical_domain = data['physical_domain']
            optional_args = data['optional_args']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            physical_domain = input_key_args()

    else:
        physical_domain = args.pop('physical_domain')
        optional_args = args

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_physical_domain(modir, physical_domain)

    modir.logout()
