from createRoutedOutside import input_key_args as input_routed_outside
from createNodesAndInterfacesProfile import input_key_args as input_node_profile
from cobra.model.l3ext import LNodeP, LIfP

from createMo import *

DEFAULT_CONSTANT = 'unspecified'

CHOICES = []


def input_key_args(msg='\nPlease input the Interface Profile info'):
    print msg
    return input_raw_input("Interface Name", required=True)


def create_interface_profile(l3ext_lnodep, interface_profile):
    """Create a The logical interface profile that defines a common configuration that will apply to one or more ports on each leaf node that is part of the containing logical node profile."""
    l3ext_lifp = LIfP(l3ext_lnodep, interface_profile)


class CreateInterfaceProfile(CreateMo):

    def __init__(self):
        self.description = 'Create a The logical interface profile that defines a common configuration that will apply to one or more ports on each leaf node that is part of the containing logical node profile.'
        self.tenant_required = True
        self.routed_outside = None
        self.node_profile = None
        self.interface_profile = None
        super(CreateInterfaceProfile, self).__init__()

    def set_cli_mode(self):
        super(CreateInterfaceProfile, self).set_cli_mode()
        self.parser_cli.add_argument('routed_outside', help='The name for the policy controlling connectivity to the outside.')
        self.parser_cli.add_argument('node_profile', help='The name of the logical node profile.')
        self.parser_cli.add_argument('interface_profile', help='The name of the logical interface profile.')

    def read_key_args(self):
        self.routed_outside = self.args.pop('routed_outside')
        self.node_profile = self.args.pop('node_profile')
        self.interface_profile = self.args.pop('interface_profile')

    def wizard_mode_input_args(self):
        self.args['routed_outside'] = input_routed_outside(msg='\nPlease input the Interface Profile info')
        self.args['node_profile'] = input_node_profile('')
        self.args['interface_profile'] = input_key_args('')

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/lnodep-' + self.node_profile + '/lifp-', self.interface_profile, LIfP, description='Interface Profile')
        super(CreateInterfaceProfile, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.check_if_tenant_exist()
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/lnodep-', self.node_profile, LNodeP, description='Node and Interface Profile')
        create_interface_profile(self.mo, self.interface_profile)

if __name__ == '__main__':
    mo = CreateInterfaceProfile()