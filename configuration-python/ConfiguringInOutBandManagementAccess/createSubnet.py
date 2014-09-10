from cobra.model.fv import Subnet

from utility import *

key_args = [{'name': 'tenant', 'help': 'Tenant name'},
            {'name': 'bridge_domain', 'help': 'Bridge Domain'},
            {'name': 'subnet', 'help': 'Subnet IP'},
            ]


def input_key_args(msg='\nPlease specify the Subnet:'):
    print msg
    args = []
    args.append(get_raw_input("Tenant name (required): ", required=True))
    args.append(get_raw_input("Bridge Domain (required): ", required=True))
    args.append(get_raw_input("Subnet IP (required): ", required=True))
    return args


def create_subnet(modir, tenant, bridge_domain, subnet):

    # Query a parent
    fv_bd = modir.lookupByDn('uni/tn-'+tenant+'/BD-'+bridge_domain)
    fv_subnet = Subnet(fv_bd, subnet)

    print_query_xml(fv_bd)
    commit_change(modir, fv_bd)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Dreate a Subnet.', key_args)
        tenant = args.pop('tenant')
        bridge_domain = args.pop('bridge_domain')
        subnet = args.pop('subnet')

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            tenant = data['tenant']
            bridge_domain = data['bridge_domain']
            subnet = data['subnet']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            tenant, bridge_domain, subnet = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_subnet(modir, tenant, bridge_domain, subnet)

    modir.logout()
