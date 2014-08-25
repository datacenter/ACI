from utility import *
from createTenant import create_tenant
from addSecurityDomain import add_security_domain
from addPrivateL3Network import add_private_l3_network
from addBridgeDomainSubnet import add_bridge_domain_subnet


if __name__ == '__main__':
    try:
        data = read_config_yaml_file(sys.argv[1])
    except IOError:
        print 'No such file or directory:', sys.argv[1]
        sys.exit()
    else:
        host_name = data['host_name']
        user_name = data['user_name']
        password = data['password']
        tenant_name = data['tenant_name']
        private_l3_network = data['private_network']
    modir = apic_login(host_name, user_name, password)

    # Create a tenant. The tenant is defined by the user.
    create_tenant(modir, tenant_name)

    # Add security domains
    for i in data['security_domain']:
        add_security_domain(modir, tenant_name, i)

    # Create private network
    add_private_l3_network(modir, tenant_name, private_l3_network)

    # Create two bridge domains. Each one contains one subnet.
    for i in data['bridge_domain']:
        add_bridge_domain_subnet(modir, tenant_name, i['name'], i['subnet_ip'], private_l3_network)
    modir.logout()
