from utility import *
from createEmptyTenant import create_tenant
from addSecurityDomain import add_security_domain
from addPrivateL3Network import add_private_l3_network
from addBridgeDomainSubnet import add_bridge_domain_subnet


def lab2(modir, tenant_name):
    """Following the Lab Guide, we create a tenant"""

    #  SystemExit:. The tenant is defined by the user.
    create_tenant(modir, tenant_name)
    # Add two security domain
    add_security_domain(modir, tenant_name, 'all')
    add_security_domain(modir, tenant_name, 'mgmt')
    # Create private network
    private_l3_network = tenant_name+'_VRF'
    add_private_l3_network(modir, tenant_name, private_l3_network)
    # Create two bridge domains. Each one contains one subnet.
    add_bridge_domain_subnet(modir, tenant_name, tenant_name+'_BD1', '10.10.10.1/24', private_l3_network)
    add_bridge_domain_subnet(modir, tenant_name, tenant_name+'_BD2', '20.20.20.1/24', private_l3_network)


if __name__ == '__main__':

    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'}]
        host_name, user_name, password, args = set_cli_argparse('Create a default tenant.', key_args)
        tenant_name = args.pop('tenant')

    except SystemExit:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')
            
        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        
    modir = apic_login(host_name, user_name, password)
    lab2(modir, tenant_name)
    modir.logout()

