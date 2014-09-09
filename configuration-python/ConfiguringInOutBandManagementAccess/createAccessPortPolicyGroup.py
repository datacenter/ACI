import re
from cobra.model.infra import AccPortGrp, RsHIfPol, RsCdpIfPol, RsLldpIfPol, RsStpIfPol, RsMonIfInfraPol, RsAttEntP, ConnNodeS, HConnPortS, ConnNodeBlk, RsConnPortS, ConnPortBlk

from utility import *

key_args = [{'name': 'group_name', 'help': 'Port Policy Group name'}]
opt_args = [{'flag': 'L', 'name': 'link_level', 'help': 'Link Level Policy'},
            {'flag': 'c', 'name': 'cdp', 'help': 'CDP Policy'},
            {'flag': 'l', 'name': 'lldp', 'help': 'LLDP Policy'},
            {'flag': 's', 'name': 'stp_interface', 'help': 'STP Interface Policy'},
            {'flag': 'm', 'name': 'monitoring', 'help': 'Monitoring Policy'},
            {'flag': 'e', 'name': 'entity_profile', 'help': 'Attached Entity Profile'},
            {'flag': 'I', 'name': 'switch_id', 'help': 'Switch ID'},
            {'flag': 'i', 'name': 'interfaces', 'help': 'Interfaces'},
]

DEFAULT_LINK_LEVEL = None
DEFAULT_CDP = None
DEFAULT_LLDP = None
DEFAULT_STP_INTERFACE = None
DEFAULT_MONITORING = None
DEFAULT_ATTACHED_ENTITY_PROFILE = None


def input_key_args(msg='\nPlease specify the Policy Group identity:'):
    print msg
    return get_raw_input("Policy Group Name (required): ", required=True)


def input_optional_args():
    args = {}
    # args['link_level'] = get_raw_input("Link Level Policy (default: None): ")
    # args['cdp'] = get_raw_input("CDP Policy (default: None): ")
    # args['lldp'] = get_raw_input("LLDP Policy (default: None): ")
    # args['stp_interface'] = get_raw_input("STP Interface Policy (default: None): ")
    # args['monitoring'] = get_raw_input("Monitoring Policy (default: None): ")
    args['entity_profile'] = get_raw_input("Attached Entity Profile (default: None): ")
    if args['entity_profile'] != '':
        args['connectivity_filters'] = add_mos(input_connectivity_filter, 'Add a Connectivity Filter')
    return args


def input_interface():
    return get_raw_input('Interface (eg: 1/14, 1/13-15, 101/13-15): ', required=True)


def input_connectivity_filter(msg='Please specify the Connectivity Filters:'):
    print msg
    args = {}
    args['switch_id'] = get_raw_input('Switch IDs (required): ', required=True)
    args['interfaces'] = add_mos(input_interface, 'Add an Interface')
    return args


def create_access_port_port_policy_group(modir, group_name, **args):

    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    # Query a parent
    infra_funcprof = modir.lookupByDn('uni/infra/funcprof/')
    infra_accportgrp = AccPortGrp(infra_funcprof, group_name)

    if check_if_key_existed(args, 'link_level'):
        infra_rshifpol = RsHIfPol(infra_accportgrp, tnFabricHIfPolName=args['link_level'])
    if check_if_key_existed(args, 'cdp'):
        infra_rscdpifpol = RsCdpIfPol(infra_accportgrp, tnCdpIfPolName=args['cdp'])
    if check_if_key_existed(args, 'lldp'):
        infra_rslldpifpol = RsLldpIfPol(infra_accportgrp, tnLldpIfPolName=args['lldp'])
    if check_if_key_existed(args, 'stp_interface'):
        infra_rsstpifpol = RsStpIfPol(infra_accportgrp, tnStpIfPolName=args['stp_interface'])
    if check_if_key_existed(args, 'monitoring'):
        infra_rsmonifinfrapol = RsMonIfInfraPol(infra_accportgrp, tnMonInfraPolName=args['monitoring'])

    if check_if_key_existed(args, 'entity_profile'):
        infra_rsattentp = RsAttEntP(infra_accportgrp, tDn='uni/infra/attentp-'+args['entity_profile'])

        def add_connectivity_filter(index, filter):
            infra_connnodes = ConnNodeS(infra_rsattentp, 'selector'+str(filter['switch_id']))
            infra_hconnports = HConnPortS(infra_rsattentp, 'selector'+str(filter['switch_id'])+'LeafPorts', 'range')
            infra_connnodeblk = ConnNodeBlk(infra_connnodes, 'block'+str(index), from_=str(filter['switch_id']), to_=str(filter['switch_id']))
            infra_rsconnports = RsConnPortS(infra_connnodes, 'uni/infra/funcprof/accportgrp-'+group_name+'/rsattEntP/hports-selector'+str(filter['switch_id'])+'LeafPorts-typ-range')
            id = 0
            for interface in filter['interfaces']:
                id += 1
                card_and_port = str(interface)
                card_and_port = re.split('/|-',card_and_port)
                card = card_and_port[0]
                fromPort = card_and_port[1]
                toPort = fromPort if len(card_and_port)<=2 else card_and_port[2]
                infra_connportblk = ConnPortBlk(infra_hconnports, 'block'+str(id), fromCard=card, toCard=card, fromPort=fromPort, toPort=toPort)

        # mode 2 and 3
        if check_if_key_existed(args, 'connectivity_filters'):
            index = 0
            for filter in args['connectivity_filters']:
                index += 1
                add_connectivity_filter(index, filter)

        # mode 1
        elif check_if_key_existed(args, 'switch_id') and check_if_key_existed(args, 'interfaces'):
            add_connectivity_filter(1, {'switch_id': args['switch_id'], 'interfaces':[args['interfaces']]})

    print_query_xml(infra_funcprof)
    commit_change(modir, infra_funcprof)


if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('create Access Port Policy Group.', key_args, opt_args)

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv, opt_args):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            group_name = data['group_name']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv) > 1:
                print input_error
            host_name, user_name, password = '172.22.233.207', 'admin', 'Cisco123' #input_login_info()
            group_name = 'bon3'#input_key_args()
            optional_args = input_optional_args()

        else:
            if 'optional_args' in data.keys():
                optional_args = data['optional_args']
            else:
                optional_args = {}
    else:
        group_name = args.pop('group_name')
        optional_args = args

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_access_port_port_policy_group(modir, group_name, args_from_CLI=optional_args)

    modir.logout()
