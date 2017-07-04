from cobra.model.dns import Profile, Domain, Prov, RsProfileToEpg

from createMo import *


DEFAULT_PREFERRED = 'false'

PREFERRED_CHOICES = ['true', 'false']
MANAGEMENT_EPG_CHOICES = ['in_band', 'out_of_band']


def input_key_args(msg='\nPlease Specify DNS profile:'):
    print msg
    return input_raw_input("DNS profile Name", required=True)


def input_dns_domain():
    return {'name': input_raw_input('DNS Domain Name', required=True),
            'is_default': input_options('Set as default', DEFAULT_PREFERRED, PREFERRED_CHOICES),
            'description': input_raw_input('Description')}
    

def input_dns_provider():
    return {'address': input_raw_input('DNS Provider Address', required=True),
            'is_preferred': input_options('Set as preferred', DEFAULT_PREFERRED, PREFERRED_CHOICES)}


def input_optional_args():
    args = {}
    args['dns_domains'] = read_add_mos_args(add_mos('Add a DNS Domain', input_dns_domain))
    args['dns_providers'] = read_add_mos_args(add_mos('Add a DNS Provider', input_dns_provider))
    args['management_epg'] = input_options('Management EPG', '', MANAGEMENT_EPG_CHOICES)
    return args


def create_dns_profile(parent_mo, dns_profile, **args):
    """Create DNS Profile"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    dns_pro = Profile(parent_mo, dns_profile)

    # add DNS Providers
    if is_valid_key(args, 'dns_providers'):
        for provider in args['dns_providers']:
            dns_prov = Prov(dns_pro, provider['address'],
                            preferred=str(get_value(provider, 'is_preferred', DEFAULT_PREFERRED)).lower())

    # add DNS Domains
    if is_valid_key(args, 'dns_domains'):
        for domain in args['dns_domains']:
            dns_domain = Domain(dns_pro, domain['name'],
                                isDefault=str(get_value(domain, 'is_default', DEFAULT_PREFERRED)).lower(),
                                descr=get_value(domain, 'description', ''))

    # set Management EPG
    if is_valid_key(args, 'management_epg'):
        if args['management_epg'].lower() == MANAGEMENT_EPG_CHOICES[0]:
            dns_rsprofiletoepg = RsProfileToEpg(dns_pro, tDn='uni/tn-mgmt/mgmtp-default/inb-default')
        elif args['management_epg'].lower() == MANAGEMENT_EPG_CHOICES[1]:
            dns_rsprofiletoepg = RsProfileToEpg(dns_pro, tDn='uni/tn-mgmt/mgmtp-default/oob-default')

    return dns_pro


class CreateDnsProfile(CreateMo):

    def __init__(self):
        self.description = 'Create DNS Profile. DNS is a distributed database with which you can map host names to IP addresses through the DNS protocol from a DNS server. When you configure DNS on the switch, you can substitute the host name for the IP address with all IP commands.'
        self.dns_profile = None
        super(CreateDnsProfile, self).__init__()

    def set_cli_mode(self):
        super(CreateDnsProfile, self).set_cli_mode()
        self.parser_cli.add_argument('dns_profile', help='The name of the DNS profile.')
        self.parser_cli.add_argument('-d', '--dns_domains', nargs=3, action='append', help='The DNS domain parameters. DNS uses a hierarchical scheme for establishing host names for network nodes, which allows local control of the segments of the network through a client-server scheme. The DNS system can locate a network device by translating the hostname of the device into its associated IP address.')
        self.parser_cli.add_argument('-p', '--dns_providers', nargs=2, action='append', help='The DNS provider information. DNS uses a hierarchical scheme for establishing host names for network nodes, which allows local control of the segments of the network through a client-server scheme. The DNS system can locate a network device by translating the hostname of the device into its associated IP address.')
        self.parser_cli.add_argument('-e', '--management_epg', choices=MANAGEMENT_EPG_CHOICES, help='Relation to DNS server endpoint group.')

    def read_key_args(self):
        self.dns_profile = self.args.pop('dns_profile')

    def wizard_mode_input_args(self):
        self.args['dns_profile'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def run_cli_mode(self):
        super(CreateDnsProfile, self).run_cli_mode()
        if is_valid_key(self.args, 'dns_providers'):
            pvds = []
            for provider in self.args['dns_providers']:
                pvds.append({
                    'address': provider[0],
                    'is_preferred': provider[1]
                })
            self.args['dns_providers'] = pvds
        if is_valid_key(self.args, 'dns_domains'):
            domains = []
            for domain in self.args['dns_domains']:
                domains.append({
                    'name': domain[0],
                    'is_default': domain[1],
                    'description': domain[2]
                })
            self.args['dns_domains'] = domains

    def delete_mo(self):
        self.check_if_mo_exist('uni/fabric/dnsp-', self.dns_profile, Profile, description='DNS Profile')
        super(CreateDnsProfile, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.look_up_mo('uni/fabric', '')
        create_dns_profile(self.mo, self.dns_profile, optional_args=self.optional_args)


if __name__ == '__main__':
    mo = CreateDnsProfile()


