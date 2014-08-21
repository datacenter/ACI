from utility import *
from cobra.model.fv import BD
from cobra.model.fv import Ctx
from cobra.model.fv import RsCtx
from cobra.model.fv import Subnet


def input_key_args(msg='Please input Bridge Domain info:'):
    print msg
    args = []
    args.append(get_raw_input("Bridge Domain (required): ", required=True))
    args.append(get_raw_input("Subnet IP (required): ", required=True))
    args.append(get_raw_input("Private L3 Network (required): ", required=True))
    return args


def add_bridge_domain_subnet(modir, tenant_name, bridge_domain, subnet_ip, network_name):
    """Build a bridge domain and its associated subnet"""

    # Query to a tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)

    # Create a bridge domain
    fv_bd = BD(fv_tenant, bridge_domain)

    # Create a subnet
    fv_subnet = Subnet(fv_bd, subnet_ip)

    # Connect the bridge domain to a network
    if isinstance(modir.lookupByDn('uni/tn-' + tenant_name + '/ctx-' + network_name), Ctx):
        fv_rsctx = RsCtx(fv_bd, tnFvCtxName=network_name)
    else:
        print 'Network', network_name, 'does not existe.'

    print_query_xml(fv_tenant)
    commit_change(modir, fv_tenant)

if __name__ == '__main__':
    if len(sys.argv) != 8:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
        bridge_domain, subnet_ip, network_name = input_key_args()
    else:
        hostname, username, password, tenant_name, bridge_domain, subnet_ip, network_name = sys.argv[1:]

    modir = apic_login(hostname, username, password)
    add_bridge_domain_subnet(modir, tenant_name, bridge_domain, subnet_ip, network_name)
    modir.logout()
