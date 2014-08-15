import sys
from utility import *
import createTenant
import addSecurityDomain
import addPrivateL3Network
import addBridgeDomainSubnet


# add a MO
def adding_a_mo(msg):
    r_input = raw_input('\n' + msg+' (y/n)? : ')
    if r_input == '':
        adding_a_mo(msg)
    return r_input.lower() in ['yes', 'y']


# add a list the the same type MOs
def add_mos(function, msg):
    mos = []
    add_one_mo = adding_a_mo(msg)
    msg = msg.replace(' a ', ' another ')
    while add_one_mo:
        mos.append(function())
        add_one_mo = adding_a_mo(msg)
    return mos


if __name__ == '__main__':

    # Login
    hostname, username, password = input_login_info(msg='')
    try:
        modir = apic_login(hostname, username, password)
        print 'Login succeed.'
    except KeyError:
        print 'Login fail.'
        sys.exit()

    # input Tenant info
    tenant_name = input_tenant_name()

    security_domain_array = add_mos(addSecurityDomain.input_key_args, 'Add a Security Domain')
    network_array = add_mos(addPrivateL3Network.input_key_args, 'Add a Private L3 Network')
    bridge_domain_array = add_mos(addBridgeDomainSubnet.input_key_args, 'Add a Bridge Domain')

    createTenant.create_tenant(modir, tenant_name)

    for security_domain in security_domain_array:
        addSecurityDomain.add_security_domain(modir, tenant_name, security_domain)
    for network in network_array:
        addPrivateL3Network.add_private_l3_network(modir, tenant_name, network)
    for bridge_domain in bridge_domain_array:
        bridge_domain_name, subnet_ip, network_name = bridge_domain
        addBridgeDomainSubnet.add_bridge_domain_subnet(modir, tenant_name, bridge_domain_name, subnet_ip, network_name)

    modir.logout()
