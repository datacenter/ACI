from createL3EpgProviderContract import create_L3_epg_provider_contract
from createL3EpgConsumerContract import create_L3_epg_consumer_contract
from configPrivateNetworkDefaultTimers import config_private_network_default_timers
from associateL3OutsideNetworkToBD import associate_l3_outside_network_to_bd

from utility import *


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Configure provider/consumer for external network epg, set setting for private network and associate the l3 outside network to a bridge domain.')
    parser.add_argument('yaml', help='Imported yaml file.')
    args = vars(parser.parse_args())

    try:
        data = read_config_yaml_file(args['yaml'], login_info=False)
    except IOError:
        print 'No such file or directory:', args['yaml']
        sys.exit()
    else:
        host, user, password = get_login_info(data)
        modir = apic_login(host, user, password)
        tenant = data['tenant']
        routed_outside = data['outside_network']
        external_network_epg = data['external_network_epg']
        provider_contract = data['provider_contract']['name']
        provider_contract_opt_args = {}
        provider_contract_opt_args['prio'] = data['provider_contract']['qos_class']
        provider_contract_opt_args['mathT'] = data['provider_contract']['match_type']
        consumer_contract = data['consumer_contract']['name']
        consumer_contract_opt_args = {}
        consumer_contract_opt_args['prio'] = data['provider_contract']['qos_class']
        private_network = data['private_network']['name']
        private_network_opt_args = {}
        private_network_opt_args['bgp'] = data['private_network']['bgp_timers']
        private_network_opt_args['ospf'] = data['private_network']['ospf_timers']
        private_network_opt_args['eprp'] = data['private_network']['end_point_retention_policy']
        private_network_opt_args['mp'] = data['private_network']['monitoring_policy']
        bridge_domain = data['bridge_domain']

    create_L3_epg_provider_contract(modir, tenant, routed_outside,
                                    external_network_epg, provider_contract,
                                    args_from_CLI=provider_contract_opt_args)

    create_L3_epg_consumer_contract(modir, tenant, routed_outside,
                                    external_network_epg, consumer_contract,
                                    args_from_CLI=consumer_contract_opt_args)

    config_private_network_default_timers(modir, tenant, private_network,
                                          args_from_CLI=private_network_opt_args)

    associate_l3_outside_network_to_bd(modir, tenant, bridge_domain,
                                       routed_outside)
