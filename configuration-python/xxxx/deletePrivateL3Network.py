from addPrivateL3Network import input_key_args, Ctx
from utility import *


def build_private_l3_network(modir, tenant_name, private_l3_network):
    """Delete a network"""
    fv_ctx = modir.lookupByDn('uni/tn-' + tenant_name + '/ctx-' + private_l3_network)

    if isinstance(fv_ctx, Ctx):
        fv_ctx.delete()
    else:
        print 'Private L3 Network', private_l3_network, 'does not existed.'
        return

    print_query_xml(fv_ctx)

    commit_change(modir, fv_ctx)

if __name__ == '__main__':

    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'private_l3_network', 'help': 'Private Network'}]
    try:
        host_name, user_name, password, args = set_cli_argparse('Delete a Private Network.', key_args)
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
    build_private_l3_network(modir, tenant_name, private_l3_network)
    modir.logout()
