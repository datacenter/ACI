from utility import *
from createEmptyTenant import create_tenant
from addSecurityDomain import add_security_domain
from addPrivateL3Network import add_private_l3_network
from addBridgeDomainSubnet import add_bridge_domain_subnet


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create a Tenant with a config file in yaml.')
    parser.add_argument('yaml', help='Imported yaml file.')
    args = vars(parser.parse_args())

    try:
        data = read_config_yaml_file(args['yaml'], login_info=False)
    except IOError:
        print 'No such file or directory:', sys.argv[1]
        sys.exit()
    else:
        host, user, password = get_login_info(data)
        tenant = data['tenant']
        private_l3_network = data['private_network']
    modir = apic_login(host, user, password)

    #  SystemExit:. The tenant is defined by the user.
    create_tenant(modir, tenant)

    # Add security domains
    for i in data['security_domain']:
        add_security_domain(modir, tenant, i)

    # Create private network
    add_private_l3_network(modir, tenant, private_l3_network)

    # Create two bridge domains. Each one contains one subnet.
    for i in data['bridge_domain']:
        add_bridge_domain_subnet(modir, tenant, i['name'], i['subnet_ip'], private_l3_network)
    modir.logout()
