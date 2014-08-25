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
    if len(sys.argv) == 6:
        host_name, user_name, password, tenant_name, private_l3_network = sys.argv[1:]
    else:
        try:
            data = read_config_yaml_file(sys.argv[1])
            host_name = data['host_name']
            user_name = data['user_name']
            password = data['password']
            tenant_name = data['tenant_name']
            private_l3_network = data['private_network']
        except (IOError, KeyError, TypeError):
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            private_l3_network = input_key_args()

    modir = apic_login(host_name, user_name, password)
    build_private_l3_network(modir, tenant_name, private_l3_network)
    modir.logout()
