import sys
import getopt
from cobra.model.fv import Tenant
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
                args['tcp_flag'], = get_optional_input('tcp Flag (default: "' + DEFAULT_TCP_FLAG + '")', ['established(e)', 'synchronize(s)', 'acknowledgment(a)', 'finish(f)', 'reset(r)'])
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

    print toXMLStr(fv_tenant, prettyPrint=True)
    commit_change(modir, fv_tenant)

if __name__ == '__main__':

    # Obtain the arguments from CLI
    opts = sys.argv[1:]
    opts.reverse()

    # Obtain the key parameters.
    keys = []
    while len(opts) > 0 and opts[len(opts)-1][0] != '-':
        keys.append(opts.pop())
    opts.reverse()
    try:
        host_name, user_name, password, tenant_name, filter_name = sys.argv[1:6]
        # Obtain the optional arguments that with a flag.
        try:
            opts, args = getopt.getopt(opts, 'an:e:i:s:S:d:D:f',
                                       ['apply-frag=', 'entry-name=', 'ether-type=', 'ip-protocol=', 'source-port-from=',
                                        'source-port-to=', 'destination-port-from=', 'destination-port-to=', 'tcp-flag='])
        except getopt.GetoptError:
            sys.exit(2)
        optional_args = {}
        for opt, arg in opts:
            if opt in ('-a', '--apply-frag'):
                optional_args['apply_frag'] = 'true'
            elif opt in ('-n', '--entry-name'):
                optional_args['entry_name'] = arg
            elif opt in ('-e', '--ether-type'):
                optional_args['ether_type'] = arg
            elif opt in ('-i', '--ip-protocol'):
                optional_args['ip_protocol'] = arg
            elif opt in ('-s', '--source-port-from'):
                optional_args['source_port_from'] = arg
            elif opt in ('-S', '--source-port-to'):
                optional_args['source_port_to'] = arg
            elif opt in ('-d', '--destination-port-from'):
                optional_args['destination_port_from'] = arg
            elif opt in ('-D', '--destination-port-to'):
                optional_args['destination_port_to'] = arg
            elif opt in ('-f', '--tcp-flag'):
                optional_args['tcp_flag'] = arg

    except ValueError:
        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        filter_name = input_key_args()
        optional_args = input_optional_args(filter_name)

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_filter(modir, tenant_name, filter_name, args_from_CLI=optional_args)

    modir.logout()


