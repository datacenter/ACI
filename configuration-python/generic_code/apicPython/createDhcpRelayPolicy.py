from cobra.model.dhcp import RelayP, RsProv

from createMo import *

EPG_TYPE_CHOICES = ['application_epg', 'l2_external_network', 'l3_external_network']
EPG_TYPE = ['Application EPG', 'L2 External Network', 'L3 External Network']


def input_key_args(msg='\nPlease Specify the DHCP Relay Policy:'):
    print msg
    return input_raw_input("DHCP Relay Profile Name", required=True)


def input_dhcp_provider(msg='\nPlease Specify the DHCP Relay Provider:'):

    print msg

    def _set_provider_detail(promt1, promt2):
        print '\nSpecify Tenant, ' + promt1 + ' and ' + promt2 + ' of the DHCP Provider:'
        return {
            'tenant':input_raw_input('Tenant', required=True),
            'detail1':input_raw_input(promt1, required=True),
            'detail2':input_raw_input(promt2, required=True)
        }

    args = {}
    args['epg_type'] = input_options('EPG Type', '', EPG_TYPE_CHOICES, required=True)
    # args['epg_type'] = EPG_TYPE[EPG_TYPE_CHOICES.index(args['ept_type'])]
    if args['epg_type'] == EPG_TYPE_CHOICES[0]:
        args['provider_detail'] = _set_provider_detail('Application Profile', 'EPG')
    elif args['epg_type'] == EPG_TYPE_CHOICES[1]:
        args['provider_detail'] = _set_provider_detail('L2 Out', 'External Network')
    elif args['epg_type'] == EPG_TYPE_CHOICES[2]:
        args['provider_detail'] = _set_provider_detail('L3 Out', 'External Network')
    args['dhcp_server_address'] = input_raw_input('DHCP Server Address', required=True)
    return args


def input_optional_args():
    args = {'providers': read_add_mos_args(
        add_mos('Add a DHCP Provider', input_dhcp_provider))}
    return args


def create_dhcp_relay_policy(parent_mo, dhcp_relay_policy, **args):
    """Create Dhcp Relay Policy"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    dhcp_relayp = RelayP(parent_mo, dhcp_relay_policy)
    if is_valid_key(args, 'providers'):
        for provider in args['providers']:
            if provider['epg_type'] == EPG_TYPE_CHOICES[0]:
                path = 'uni/tn-'+provider['provider_detail']['tenant']+'/ap-'+provider['provider_detail']['detail1']+'/epg-'+provider['provider_detail']['detail2']
            elif provider['epg_type'] == EPG_TYPE_CHOICES[1]:
                path = 'uni/tn-'+provider['provider_detail']['tenant']+'/l2out-'+provider['provider_detail']['detail1']+'/instP-'+provider['provider_detail']['detail2']
            elif provider['epg_type'] == EPG_TYPE_CHOICES[2]:
                path = 'uni/tn-'+provider['provider_detail']['tenant']+'/out-'+provider['provider_detail']['detail1']+'/instP-'+provider['provider_detail']['detail2']
            else:
                print 'Not a valid EPG Type. Please try again.'
                sys.exit()
            dhcp_rsprov = RsProv(dhcp_relayp, path, addr=provider['dhcp_server_address'])
    return dhcp_relayp


class CreateDhcpRelayPolicy(CreateMo):

    def __init__(self):
        self.description = 'Create Dhcp Relay Policy. Configure a DHCP relay profile, with one or more helper addresses in it, to configure a DHCP relay agent for forwarding DHCP packets to a remote server. '
        self.tenant_required = True
        self.dhcp_relay_policy = None
        super(CreateDhcpRelayPolicy, self).__init__()

    def set_cli_mode(self):
        super(CreateDhcpRelayPolicy, self).set_cli_mode()
        self.parser_cli.add_argument('dhcp_relay_policy', help='The DHCP relay policy name.')
        self.parser_cli.add_argument('-p', '--providers', nargs=5, action='append', help='A relation to an endpoint group. A relationship from a DHCP relay profile to an endpoint group is required for clients in the endpoint group to acquire IP addresses using the DHCP profile. Once the relationship is set up, any host in the endpoint group can obtain the IP address from the DHCP server.')

    def read_key_args(self):
        self.dhcp_relay_policy = self.args.pop('dhcp_relay_policy')

    def wizard_mode_input_args(self):
        self.args['dhcp_relay_policy'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def run_cli_mode(self):
        super(CreateDhcpRelayPolicy, self).run_cli_mode()
        if is_valid_key(self.args, 'providers'):
            pvds = []
            for provider in self.args['providers']:
                pvds.append({
                    'epg_type': provider[0],
                    'provider_detail': {
                        'tenant': provider[1],
                        'detail1': provider[2],
                        'detail2': provider[3]
                    },
                    'dhcp_server_address': provider[4]
                })
            self.args['providers'] = pvds

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-'+self.tenant+'/relayp-', self.dhcp_relay_policy, RelayP, description='DHCP Relay Policy')
        super(CreateDhcpRelayPolicy, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.check_if_tenant_exist()
        create_dhcp_relay_policy(self.mo, self.dhcp_relay_policy, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateDhcpRelayPolicy()


