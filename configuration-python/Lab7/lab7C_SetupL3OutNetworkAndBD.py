from createL3EpgProviderContract import create_L3_epg_provider_contract
from createL3EpgConsumerContract import create_L3_epg_consumer_contract
from configPrivateL3NetworkDefaultTimers import config_private_l3_network_default_timers
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
    config_private_l3_network_default_timers(modir, tenant_name, private_network, ospf='default')
    associate_l3_outside_network_to_bd(modir, tenant_name, bridge_domain, routed_outside_name)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
    else:
        hostname, username, password, tenant_name = sys.argv[1:]
    modir = apic_login(hostname, username, password)
    lab7B(modir, tenant_name)
    modir.logout()
