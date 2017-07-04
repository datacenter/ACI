from cobra.model.fv import BD
from cobra.model.dhcp import Lbl, RsDhcpOptionPol, RelayP

from createBridgeDomain import input_key_args as input_bridge_domain

from createMo import *

DHCP_LABEL_SCOPE_CHOICES = ['infra', 'tenant']


def input_key_args(msg='\nPlease Specify the DHCP Relay Label:', delete_function=False):
    print msg
    args = [input_raw_input("DHCP Relay Label Name", required=True)]
    if not delete_function:
        input_options('DHCP Label Scope', '', DHCP_LABEL_SCOPE_CHOICES, required=True),
    else:
        args.extend([None])
    return args


def input_optional_args():
    args = {'dhcp_option_policy': input_raw_input('DHCP Option Policy')}
    return args


def create_dhcp_relay_label(parent_mo, dhcp_relay_label_scope, dhcp_relay_label_name, **args):
    """Create a Dhcp Relay Label"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    dhcp_lbl = Lbl(parent_mo, dhcp_relay_label_name, owner=dhcp_relay_label_scope)

    if is_valid_key(args, 'dhcp_option_policy'):
        dhcp_= RsDhcpOptionPol(dhcp_lbl,
                               tnDhcpOptionPolName=args['dhcp_option_policy'])
    return dhcp_lbl

class CreateDhcpRelayLabel(CreateMo):

    def __init__(self):
        self.description = 'Create a Dhcp Relay Label. The DHCP relay label contains a name for the label, the scope, and a DHCP option policy. The scope is the owner of the relay server and the option policy supplies DHCP clients with configuration parameters, such as domain, nameserver, and subnet router addresses.'
        self.tenant_required = True
        self.bridge_domain = None
        self.dhcp_relay_label_scpoe = None
        self.dhcp_relay_label_name = None
        super(CreateDhcpRelayLabel, self).__init__()

    def set_cli_mode(self):
        super(CreateDhcpRelayLabel, self).set_cli_mode()
        self.parser_cli.add_argument('bridge_domain', help='Bridge Domain Name')
        self.parser_cli.add_argument('dhcp_relay_label_name', help='DHCP Relay Label Name.')
        self.parser_cli.add_argument('dhcp_relay_label_scope', choices = DHCP_LABEL_SCOPE_CHOICES, help='Represents the target relay servers ownership.')
        self.parser_cli.add_argument('-p', '--dhcp_option_policy', help='Relation to the DHCP option policy.')

    def read_key_args(self):
        self.bridge_domain = self.args.pop('bridge_domain')
        self.dhcp_relay_label_name = self.args.pop('dhcp_relay_label_name')
        self.dhcp_relay_label_scope = self.args.pop('dhcp_relay_label_scope')

    def wizard_mode_input_args(self):
        self.args['bridge_domain'] = input_bridge_domain('\nPlease Specify the DHCP Relay Label:', delete_function=True)[0]
        self.args['dhcp_relay_label_name'], self.args['dhcp_relay_label_scope'] = input_key_args('', delete_function=self.delete)
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-'+self.tenant+'/BD-'+self.bridge_domain+'/dhcplbl-', self.dhcp_relay_label_name, Lbl, description='DHCP Relay Label')
        super(CreateDhcpRelayLabel, self).delete_mo()

    def main_function(self):
        # check if DHCP Relay Policy exist
        self.check_if_mo_exist('uni/tn-'+self.tenant+'/relayp-', self.dhcp_relay_label_name, RelayP, description='DHCP Relay Policy')
        # Query a parent
        self.check_if_mo_exist('uni/tn-'+self.tenant+'/BD-', self.bridge_domain, BD, 'Bridge Domain')
        create_dhcp_relay_label(self.mo, self.dhcp_relay_label_scope, self.dhcp_relay_label_name, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateDhcpRelayLabel()


