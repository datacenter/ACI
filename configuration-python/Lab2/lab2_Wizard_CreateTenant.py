import sys
from utility import *
import createTenant
import addSecurityDomain
import addPrivateL3Network
import addBridgeDomainSubnet


if __name__ == '__main__':

    # Login
    hostname, username, password = input_login_info(msg='')
    try:
        modir = apic_login(hostname, username, password)
        print 'Login succeed.'
    except KeyError:
        print 'Login fail.'
        sys.exit()

    # Wizard starts asking inputs step by step
    tenant_name = input_tenant_name()
    security_domain_array = add_mos(addSecurityDomain.input_key_args, 'Add a Security Domain')
    network_array = add_mos(addPrivateL3Network.input_key_args, 'Add a Private L3 Network')
    bridge_domain_array = add_mos(addBridgeDomainSubnet.input_key_args, 'Add a Bridge Domain')

    # Running
    createTenant.create_tenant(modir, tenant_name)
    for security_domain in security_domain_array:
        addSecurityDomain.add_security_domain(modir, tenant_name, security_domain)
    for network in network_array:
        addPrivateL3Network.add_private_l3_network(modir, tenant_name, network)
    for bridge_domain in bridge_domain_array:
        bridge_domain_name, subnet_ip, network_name = bridge_domain
        addBridgeDomainSubnet.add_bridge_domain_subnet(modir, tenant_name, bridge_domain_name, subnet_ip, network_name)

    modir.logout()
