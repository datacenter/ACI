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
    if len(sys.argv) != 6:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
        private_l3_network = input_key_args()
    else:
        hostname, username, password, tenant_name, private_l3_network = sys.argv[1:]
    modir = apic_login(hostname, username, password)
    build_private_l3_network(modir, tenant_name, private_l3_network)
    modir.logout()
