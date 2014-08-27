from createL3EpgProviderContract import create_L3_epg_provider_contract
from createL3EpgConsumerContract import create_L3_epg_consumer_contract
from configPrivateNetworkDefaultTimers import config_private_network_default_timers
from associateL3OutsideNetworkToBD import associate_l3_outside_network_to_bd

from utility import *

PROVIDER_CONTRACT_NAME = 'default'
CONSUMER_CONTRACT_NAME = 'default'
L3_NETWORK = 'L3-Out'
EXTERNAL_NETWORK_NAME = 'L3-Out-EPG'
PRIVATE_NETWORK = 'VRF'
BRIDGE_DOMAIN = 'BD1'

def lab7B(modir, tenant_name):
    """Setup the Pod Policies."""

    routed_outside_name = tenant_name+'-'+L3_NETWORK
    private_network = tenant_name+'_'+PRIVATE_NETWORK
    bridge_domain = tenant_name+'_'+BRIDGE_DOMAIN

    create_L3_epg_provider_contract(modir, tenant_name, routed_outside_name, EXTERNAL_NETWORK_NAME, PROVIDER_CONTRACT_NAME)
    create_L3_epg_consumer_contract(modir, tenant_name, routed_outside_name, EXTERNAL_NETWORK_NAME, CONSUMER_CONTRACT_NAME)
    config_private_network_default_timers(modir, tenant_name, private_network, ospf='default')
    associate_l3_outside_network_to_bd(modir, tenant_name, bridge_domain, routed_outside_name)

if __name__ == '__main__':

    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'}]
        host_name, user_name, password, args = set_cli_argparse('Create a default tenant.', key_args)
        tenant_name = args.pop('tenant')

    except: #?error

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()

    modir = apic_login(host_name, user_name, password)
    lab7B(modir, tenant_name)
    modir.logout()