from cobra.model.infra import AccPortP, HPortS, PortBlk, RsAccBaseGrp, NodeP, LeafS, NodeBlk, RsAccPortP

from utility import *

DEFAULT_INTERFACE_TYPE = 'individual'
DEFAULT_TYPE = 'range'

key_args = [{'name': 'switch_profile', 'help': 'Switch Profile Name'},
            # {'name': 'switches', 'help': 'Switches ID'},
            # {'name': 'interface_type', 'help': 'Interface Type', 'choices': ['individual', 'pc', 'vpc']},
            # {'name': 'ports', 'help': 'Interfaces Ports'},
            {'name': 'selector', 'help': 'Interface Selector Name'},
            {'name': 'policy_group', 'help': 'Interface Policy Group'},
    ]



def input_key_args(msg='', from_delete_function=False):
    print msg
    args = []
    args.append(get_raw_input("Switch Profile Name (required): ", required=True))
    if not from_delete_function:
        def input_switches():
            return get_raw_input("Switches ID (required): ", required=True)

        def input_ports():
            return get_raw_input("Interfaces Ports (required): ", required=True)

        args.append(add_mos(input_switches, 'Add a Switch?', do_first=True))
        # args.append(get_optional_input("Interface Type (default: " + DEFAULT_INTERFACE_TYPE + "): ", ['individual(i)', 'pc(p)', 'vpc(v)']))
        args.append(add_mos(input_ports, 'Add a Port?', do_first=True))
        args.append(get_raw_input("Interface Selector Name (required): ", required=True))
        args.append(get_raw_input("Interface Policy Group (required): ", required=True))
    return args


def configure_interface_pc_and_vpc(modir, switches, switch_profile, ports, selector, policy_group):

    # Query a parent
    infra = modir.lookupByDn('uni/infra')
    infra_accportp = AccPortP(infra, switch_profile + '_ifselector')
    infra_hports = HPortS(infra_accportp, selector + '_selector', DEFAULT_TYPE)
    block = 0
    for port in ports:
        block += 1
        card, fromPort, toPort = get_numbers(port)
        infra_portblk = PortBlk(infra_hports, 'block'+str(block), fromCard=card, fromPort=fromPort, toPort=toPort)
    infra_rsaccbasegrp = RsAccBaseGrp(infra_hports, tDn='uni/infra/funcprof/accportgrp-'+policy_group)

    infra_nodep = NodeP(infra, switch_profile)
    infra_leafs = LeafS(infra_nodep, switch_profile+'_selector_'+''.join(map(str,switches)), DEFAULT_TYPE)
    single = 0
    for switch in switches:
        single += 1
        infra_nodeblk = NodeBlk(infra_leafs, 'single'+str(single), from_=str(switch), to_=str(switch))

    infra_rsaccportp = RsAccPortP(infra_nodep, 'uni/infra/accportprof-'+switch_profile+'_ifselector')

    print_query_xml(infra)
    commit_change(modir, infra)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        parser = set_cli_argparse('Configure Interface PC and VPC.', key_args, return_parser=True)
        parser.add_argument('-s', '--switches', nargs="*", help='Switches ID (could be more than 1)')
        parser.add_argument('-p', '--ports', nargs="*", help='Interfaces Ports (eg: 1/12, 1/15-18, 101/32)')
        args = vars(parser.parse_args())
        host_name = args.pop('host')
        user_name = args.pop('user')
        password = args.pop('password')
        switches = args.pop('switches')
        switch_profile = args.pop('switch_profile')
        # interface_type = args.pop('interface_type')
        ports = args.pop('ports')
        selector = args.pop('selector')
        policy_group = args.pop('policy_group')

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            switches = data['switches']
            switch_profile = data['switch_profile']
            # interface_type = data['interface_type']
            ports = data['ports']
            selector = data['selector']
            policy_group = data['policy_group']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            switch_profile, switches, ports, selector, policy_group = input_key_args()


    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    configure_interface_pc_and_vpc(modir, switches, switch_profile, ports, selector, policy_group)

    modir.logout()
