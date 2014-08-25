from utility import *
from cobra.model.fv import BD
from cobra.model.fv import Ctx
from cobra.model.fv import RsCtx
from cobra.model.fv import Subnet

from addPrivateL3Network import input_key_args as input_private_network


def input_key_args(msg='Please input Bridge Domain info:'):
    print msg
    args = []
    args.append(get_raw_input("Bridge Domain (required): ", required=True))
    args.append(get_raw_input("Subnet IP (required): ", required=True))
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
    if len(sys.argv) == 8:
        host_name, user_name, password, tenant_name, bridge_domain, subnet_ip, network_name = sys.argv[1:]
    else:
        try:
            data = read_config_yaml_file(sys.argv[1])
            host_name = data['host_name']
            user_name = data['user_name']
            password = data['password']
            tenant_name = data['tenant_name']
            network_name = data['private_network']
            bridge_domain = data['bridge_domain']['name']
            subnet_ip = data['bridge_domain']['subnet_ip']
        except (IOError, KeyError, TypeError):
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            network_name = input_private_network()
            bridge_domain, subnet_ip = input_key_args()


    modir = apic_login(host_name, user_name, password)
    add_bridge_domain_subnet(modir, tenant_name, bridge_domain, subnet_ip, network_name)
    modir.logout()
