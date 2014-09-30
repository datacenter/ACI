from cobra.model.fv import Ctx

from utility import *


def input_key_args(msg='Please input Private L3 Network info:'):
    print msg
    return get_raw_input("Private L3 Network (required): ", required=True)


def add_private_l3_network(modir, tenant_name, private_l3_network):
    """Build a private L3 network"""

    # Query a tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)

    # create a private network
    fv_ctx = Ctx(fv_tenant, private_l3_network)

    print_query_xml(fv_tenant)
    commit_change(modir, fv_tenant)

if __name__ == '__main__':

    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'private_l3_network', 'help': 'Private Network'}]
    try:
        host_name, user_name, password, args = set_cli_argparse('Create a Private Network.', key_args)
        tenant_name = args.pop('tenant')
        private_l3_network = args.pop('private_l3_network')

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            tenant_name = data['tenant']
            private_l3_network = data['private_network']
        except (IOError, KeyError, TypeError, IndexError):
            if len(sys.argv)>1:
                print 'Invalid input arguments.'
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            private_l3_network = input_key_args()

    modir = apic_login(host_name, user_name, password)
    add_private_l3_network(modir, tenant_name, private_l3_network)
    modir.logout()
