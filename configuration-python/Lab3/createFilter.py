from cobra.model.vz import Filter, Entry

from utility import *

DEFAULT_ETHER_TYPE = 'unspecified'
DEFAULT_ARP_FLAG = 'unspecified'
DEFAULT_IP_PROTOCOL = 'unspecified'
DEFAULT_APPLY_FRAG = 'false'
DEFAULT_SOURCE_PORT_FROM = 'unspecified'
DEFAULT_SOURCE_PORT_TO = 'unspecified'
DEFAULT_DESTINATION_PORT_FROM = 'unspecified'
DEFAULT_DESTINATION_PORT_TO = 'unspecified'
DEFAULT_TCP_FLAG = 'unspecified'


def input_key_args(msg='\nPlease input Filter info:'):
    print msg
    return get_raw_input("Filter Name (required): ", required=True)


def input_optional_args(filter_name):
    args = {}
    args['entry_name'], = get_raw_input('Entry Name (default: "' + filter_name.lower() + '"): '),
    args['ether_type'], = get_optional_input('Ether Type (default: "' + DEFAULT_ETHER_TYPE + '")', ['trill(t)', 'arp(a)', 'mpls_unicast(mp)', 'mac_security(ma)', 'fcoe(f)', 'ip(i)']),
    if args['ether_type'] == 'arp':
        args['arp_flag'], = get_optional_input('ARP Flag (default: "' + DEFAULT_ETHER_TYPE + '")', ['true(t)', 'false(f)']),
    elif args['ether_type'] == 'ip':
        args['ip_protocol'], = get_optional_input('IP Protocol (default: "' + DEFAULT_IP_PROTOCOL + '")', ['icmp', 'igmp', 'tcp', 'egp', 'igp', 'udp', 'eigrp', 'ospf', 'pim', 'l2tp']),
        if args['ip_protocol'] in ['tcp', 'udp']:
            args['source_port_from'], = get_optional_input('Source Port From (default: "' + DEFAULT_SOURCE_PORT_FROM + '")', ['ftp-data', 'smtp', 'dns', 'http', 'pop3', 'https', 'rtsp', '(port_number)'], num_accept=True),
            args['source_port_to'], = get_optional_input('Source Port To (default: "' + DEFAULT_SOURCE_PORT_TO + '")', ['ftp-data', 'smtp', 'dns', 'http', 'pop3', 'https', 'rtsp', '(port_number)'], num_accept=True),
            args['destination_port_from'], = get_optional_input('Destination Port From (default: "' + DEFAULT_DESTINATION_PORT_FROM + '")', ['ftp-data', 'smtp', 'dns', 'http', 'pop3', 'https', 'rtsp', '(port_number)'], num_accept=True),
            args['destination_port_to'], = get_optional_input('Destination Port To (default: "' + DEFAULT_DESTINATION_PORT_TO + '")', ['ftp-data', 'smtp', 'dns', 'http', 'pop3', 'https', 'rtsp', '(port_number)'], num_accept=True),
            if args['ip_protocol'] == 'tcp':
                args['tcp_flag'] = get_optional_input('tcp Flag (default: "' + DEFAULT_TCP_FLAG + '")', ['unspecified', 'est(Established)', 'syn(Synchronize)', 'ack(Acknowledgment)', 'fin(Finish)', 'rst(Reset)'])
        else:
            args['apply_frag'], = get_optional_input('Apply frag (default: "' + DEFAULT_APPLY_FRAG + '")', ['true(t)', 'false(f)']),
    return args


def create_filter(modir, tenant_name, filter_name, **args):
    """Create a filter"""

    # Query a tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args

    # Check if the tenant exists
    if isinstance(fv_tenant, Tenant):
        # Create filter
        vz_filter = Filter(fv_tenant, filter_name)

        # Add an entry to the filter
        vz_entry = Entry(vz_filter,  get_value(args, 'entry_name', filter_name.lower()),
                         etherT=get_value(args, 'ether_type', DEFAULT_ETHER_TYPE).lower(),
                         prot=get_value(args, 'ip_protocol', DEFAULT_IP_PROTOCOL).lower(),
                         applyToFrag=get_value(args, 'apply_frag', DEFAULT_APPLY_FRAG),
                         sFromPort=get_value(args, 'source_port_from', DEFAULT_SOURCE_PORT_FROM),
                         sToPort=get_value(args, 'source_port_to', DEFAULT_SOURCE_PORT_TO),
                         dFromPort=get_value(args, 'destination_port_from', DEFAULT_DESTINATION_PORT_FROM),
                         dToPort=get_value(args, 'destination_port_to', DEFAULT_DESTINATION_PORT_TO),
                         tcpRules=get_value(args, 'tcp_flag', DEFAULT_TCP_FLAG))

    else:
        print 'Tenant', tenant_name, 'does not exist. Please create a tenant first'
        return

    print_query_xml(fv_tenant)
    commit_change(modir, fv_tenant)

if __name__ == '__main__':

    # Obtain the arguments from CLI
    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'filter', 'help': 'Filter name'}
        ]
        opt_args = [{'flag': 'a', 'name': 'apply_frag', 'default': DEFAULT_APPLY_FRAG, 'help': 'Apply to Frag'},
                    {'flag': 'n', 'name': 'entry_name',  'help': 'The name of a filter entry'},
                    {'flag': 'e', 'name': 'ether_type', 'default': DEFAULT_ETHER_TYPE, 'help': 'Ether type'},
                    {'flag': 'i', 'name': 'ip_protocol', 'default': DEFAULT_IP_PROTOCOL, 'help': 'L3 Ip Protocol'},
                    {'flag': 's', 'name': 'source_port_from', 'default': DEFAULT_SOURCE_PORT_FROM, 'help': 'Source From Port'},
                    {'flag': 'S', 'name': 'source_port_to', 'default': DEFAULT_SOURCE_PORT_TO, 'help': 'Source To Port'},
                    {'flag': 'd', 'name': 'destination_port_from', 'default': DEFAULT_DESTINATION_PORT_FROM, 'help': 'Destination From Port'},
                    {'flag': 'D', 'name': 'destination_port_to', 'default': DEFAULT_DESTINATION_PORT_TO, 'help': 'Destination To Port'},
                    {'flag': 'f', 'name': 'tcp_flag', 'default': DEFAULT_TCP_FLAG, 'help': 'TCP Session Rules'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Create a Filter.', key_args, opt_args)
        tenant_name = args.pop('tenant')
        filter_name = args.pop('filter')
        optional_args = args

    except SystemExit:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        try:
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            tenant_name = data['tenant']
            filter_name = data['filter']
            optional_args = data['optional_args']
        except (IOError, KeyError, TypeError, IndexError):
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            filter_name = input_key_args()
            optional_args = input_optional_args(filter_name)

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_filter(modir, tenant_name, filter_name, args_from_CLI=optional_args)

    modir.logout()


