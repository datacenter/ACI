from cobra.model.fv import BD, RsBDToOut
from cobra.model.l3ext import Out
from createBridgeDomainSubnet import input_key_args as input_bridge_domain
from createRoutedOutside import input_key_args as input_L3_outside_network

from createMo import *


def input_key_args(msg=''):
    print msg
    return input_bridge_domain(delete_function=True)[0]


def associate_l3_outside_network_to_bd(fv_bd, routed_outside):
    """A relation to the policy controlling connectivity to the outside. This is an internal object. """
    fv_rsbdtoout = RsBDToOut(fv_bd, routed_outside)


class AssociateL3OutsideNetworkToBD(CreateMo):

    def __init__(self):
        self.description = 'A relation to the policy controlling connectivity to the outside. This is an internal object. '
        self.tenant_required = True
        self.bridge_domain = None
        self.routed_outside = None
        super(AssociateL3OutsideNetworkToBD, self).__init__()

    def set_cli_mode(self):
        super(AssociateL3OutsideNetworkToBD, self).set_cli_mode()
        self.parser_cli.add_argument('bridge_domain', help='Bridge Domain Name')
        self.parser_cli.add_argument('routed_outside', help='The name for the policy controlling connectivity to the outside.')

    def read_key_args(self):
        self.bridge_domain = self.args.pop('bridge_domain')
        self.routed_outside = self.args.pop('routed_outside')

    def wizard_mode_input_args(self):
        self.args['bridge_domain'] = input_key_args()
        self.args['routed_outside'] = input_L3_outside_network('')

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/BD-' + self.bridge_domain + '/rsBDToOut-', self.routed_outside, RsBDToOut, description='')
        super(AssociateL3OutsideNetworkToBD, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.check_if_tenant_exist()
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-', self.routed_outside, Out, description='The policy')
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/BD-', self.bridge_domain, BD, description='Bridge Domain')
        associate_l3_outside_network_to_bd(self.mo, self.routed_outside)

if __name__ == '__main__':
    mo = AssociateL3OutsideNetworkToBD()