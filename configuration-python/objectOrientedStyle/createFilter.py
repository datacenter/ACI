from cobra.model.vz import Filter, Entry
from createMo import *

DEFAULT_ETHER_TYPE = 'unspecified'
DEFAULT_ARP_FLAG = 'unspecified'
DEFAULT_IP_PROTOCOL = 'unspecified'
DEFAULT_APPLY_FRAG = 'false'
DEFAULT_SOURCE_PORT_FROM = 'unspecified'
DEFAULT_SOURCE_PORT_TO = 'unspecified'
DEFAULT_DESTINATION_PORT_FROM = 'unspecified'
DEFAULT_DESTINATION_PORT_TO = 'unspecified'
DEFAULT_TCP_FLAG = 'unspecified'

ETHER_TYPE_CHOICES = ['trill', 'arp', 'mpls_unicast', 'mac_security', 'fcoe', 'ip']
ARP_FLAG_CHOICES = ['unspecified', 'req', 'reply']
IP_PROTOCOL_CHOICES = ['icmp', 'igmp', 'tcp', 'egp', 'igp', 'udp', 'eigrp', 'ospf', 'pim', 'l2tp']
PORT_CHOICES = ['ftp-data', 'smtp', 'dns', 'http', 'pop3', 'https', 'rtsp']
TCP_FLAG_CHOICES = ['unspecified', 'est', 'syn', 'ack', 'fin', 'rst']
APPLY_FRAG_CHOICES = ['true', 'false']

def input_key_args(msg='\nPlease input Filter info:'):
    print msg
    return input_raw_input("Filter Name", required=True)


def input_optional_args(filter_name):
    args = {}
    args['entry_name'], = input_raw_input('Entry Name', default=filter_name.lower()),
    args['ether_type'], = input_options('Ether Type', DEFAULT_ETHER_TYPE, ETHER_TYPE_CHOICES),
    if args['ether_type'] == 'arp':
        args['arp_flag'], = input_options('ARP Flag', DEFAULT_ARP_FLAG, APPLY_FRAG_CHOICES),
    elif args['ether_type'] == 'ip':
        args['ip_protocol'], = input_options('IP Protocol', DEFAULT_IP_PROTOCOL, IP_PROTOCOL_CHOICES),
        if args['ip_protocol'] in ['tcp', 'udp']:
            args['source_port_from'], = input_options('Source Port From', DEFAULT_SOURCE_PORT_FROM, PORT_CHOICES+['(port_number)'], num_accept=True),
            args['source_port_to'], = input_options('Source Port To', DEFAULT_SOURCE_PORT_TO, PORT_CHOICES+['(port_number)'], num_accept=True),
            args['destination_port_from'], = input_options('Destination Port From', DEFAULT_DESTINATION_PORT_FROM, PORT_CHOICES+['(port_number)'], num_accept=True),
            args['destination_port_to'], = input_options('Destination Port To', DEFAULT_DESTINATION_PORT_TO, PORT_CHOICES+['(port_number)'], num_accept=True),
            if args['ip_protocol'] == 'tcp':
                args['tcp_flag'] = input_options('tcp Flag', DEFAULT_TCP_FLAG, TCP_FLAG_CHOICES)
        else:
            args['apply_frag'], = input_options('Apply frag', DEFAULT_APPLY_FRAG, APPLY_FRAG_CHOICES),
    return args


def create_filter(fv_tenant, filter, **args):
    """Create a filter"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create filter
    vz_filter = Filter(fv_tenant, filter)

    # Add an entry to the filter
    vz_entry = Entry(vz_filter, get_value(args, 'entry_name', filter.lower()),
                     etherT=get_value(args, 'ether_type', DEFAULT_ETHER_TYPE).lower(),
                     prot=get_value(args, 'ip_protocol', DEFAULT_IP_PROTOCOL).lower(),
                     arpOpc=get_value(args, 'arp_flag', DEFAULT_ARP_FLAG).lower(),
                     applyToFrag=get_value(args, 'apply_frag', DEFAULT_APPLY_FRAG),
                     sFromPort=get_value(args, 'source_port_from', DEFAULT_SOURCE_PORT_FROM),
                     sToPort=get_value(args, 'source_port_to', DEFAULT_SOURCE_PORT_TO),
                     dFromPort=get_value(args, 'destination_port_from', DEFAULT_DESTINATION_PORT_FROM),
                     dToPort=get_value(args, 'destination_port_to', DEFAULT_DESTINATION_PORT_TO),
                     tcpRules=get_value(args, 'tcp_flag', DEFAULT_TCP_FLAG))

class CreateFilter(CreateMo):
    """
    Create a Filter
    """
    def __init__(self):
        self.description = 'Create a Filter'
        self.tenant_required = True
        self.filter = None
        super(CreateFilter, self).__init__()

    def set_cli_mode(self):
        super(CreateFilter, self).set_cli_mode()
        self.parser_cli.add_argument('filter', help='Filter Name')
        self.parser_cli.add_argument('-a', '--apply_frag', default= DEFAULT_APPLY_FRAG, choices=APPLY_FRAG_CHOICES, help='Apply to Frag')
        self.parser_cli.add_argument('-n', '--entry_name', help='The name of a filter entry')
        self.parser_cli.add_argument('-e', '--ether_type', default= DEFAULT_ETHER_TYPE, choices=ETHER_TYPE_CHOICES, help='Ether type')
        self.parser_cli.add_argument('-i', '--ip_protocol', default= DEFAULT_IP_PROTOCOL, choices=IP_PROTOCOL_CHOICES, help='L3 Ip Protocol')
        self.parser_cli.add_argument('-A', '--arp_flag', default= DEFAULT_ARP_FLAG, choices=APPLY_FRAG_CHOICES, help='ARP opcodes')
        self.parser_cli.add_argument('-s', '--source_port_from', default= DEFAULT_SOURCE_PORT_FROM, help='Source From Port')
        self.parser_cli.add_argument('-S', '--source_port_to', default= DEFAULT_SOURCE_PORT_TO, help='Source To Port')
        self.parser_cli.add_argument('-d', '--destination_port_from', default= DEFAULT_DESTINATION_PORT_FROM, help='Destination From Port')
        self.parser_cli.add_argument('-D', '--destination_port_to', default= DEFAULT_DESTINATION_PORT_TO, help='Destination To Port')
        self.parser_cli.add_argument('-f', '--tcp_flag', default= DEFAULT_TCP_FLAG, choices=TCP_FLAG_CHOICES ,help='TCP Session Rules: est for Established; syn for Synchronize; ack for Acknowledgment; fin for Finish; rst for Reset')

    def run_cli_mode(self):
        super(CreateFilter, self).run_cli_mode()
        self.filter = self.args.pop('filter')
        self.optional_args = self.args

    def run_yaml_mode(self):
        super(CreateFilter, self).run_yaml_mode()
        self.filter = self.args['filter']
        self.optional_args = self.args['optional_args']

    def run_wizard_mode(self):
        super(CreateFilter, self).run_wizard_mode()
        self.filter = input_key_args()
        if not self.delete:
            self.optional_args = input_optional_args(self.filter)

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-'+self.tenant+'/flt-', self.filter, Filter, description='Filter')
        super(CreateFilter, self).delete_mo()

    def createFilter(self):
        # Query a tenant
        fv_tenant = self.check_if_tenant_exist()
        create_filter(fv_tenant, self.filter, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateFilter()