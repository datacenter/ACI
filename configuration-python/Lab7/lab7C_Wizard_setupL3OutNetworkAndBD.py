import createRoutedOutside
import createExternalNetwork
import createL3EpgProviderContract
import createL3EpgConsumerContract
import configPrivateL3NetworkDefaultTimers
import associateL3OutsideNetworkToBD


from utility import *


if __name__ == '__main__':

    # Login
    hostname, username, password = '172.22.233.207', 'admin', 'Cisco123' #input_login_info(msg='')
    try:
        modir = apic_login(hostname, username, password)
        print 'Login succeed.'
    except KeyError:
        print 'Login fail.'
        sys.exit()

    # Wizard starts asking inputs step by step
    tenant_name = input_tenant_name()
    routed_outside_name = createRoutedOutside.input_key_args()
    external_network = createExternalNetwork.input_key_args()
    provider_contract_name = createL3EpgProviderContract.input_key_args()
    consumer_contract_name = createL3EpgConsumerContract.input_key_args()
    private_l3_network = configPrivateL3NetworkDefaultTimers.input_key_args()
    private_l3_network_optional_args = configPrivateL3NetworkDefaultTimers.input_optional_args()
    bridge_domain = associateL3OutsideNetworkToBD.input_key_args()

    # Running
    createL3EpgProviderContract.create_L3_epg_provider_contract(modir, tenant_name, routed_outside_name, external_network, provider_contract_name)
    createL3EpgConsumerContract.create_L3_epg_consumer_contract(modir, tenant_name, routed_outside_name, external_network, consumer_contract_name)
    configPrivateL3NetworkDefaultTimers.config_private_l3_network_default_timers(modir, tenant_name, private_l3_network, args_from_CLI=private_l3_network_optional_args)
    associateL3OutsideNetworkToBD.associate_l3_outside_network_to_bd(modir, tenant_name, bridge_domain, external_network)

