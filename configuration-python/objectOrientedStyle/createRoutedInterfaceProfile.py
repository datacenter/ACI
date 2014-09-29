from createRoutedOutside import input_key_args as input_routed_outside
from createNodesAndInterfacesProfile import input_key_args as input_node_profile
from createInterfaceProfile import input_key_args as input_interface_profile
from cobra.model.l3ext import Out, LNodeP, LIfP, RsPathL3OutAtt
from cobra.model.ospf import IfP

from createMo import *

DEFAULT_MTU = 'inherit'
DEFAULT_TARGET_DSCP = 'unspecified'


def input_key_args(msg='\nPlease Specify Routed Interface Profile:', delete_function=False):
    print msg
    key_args = []
    key_args.append(input_raw_input("Leaf ID", required=True))
    key_args.append(input_raw_input("Eth number", required=True))
    if not delete_function:
        key_args.append(input_raw_input("IP address", required=True))
    else:
        key_args.extend([None])
    return key_args


def input_optional_args(*arg):
    args = {}
    args['mtu'] = input_options('MTU', DEFAULT_MTU, [], num_accept=True)
    args['target_dscp'] = input_options('Target DSCP', DEFAULT_TARGET_DSCP, [], num_accept=True)
    return args


def create_routed_interface_profile(l3ext_lifp, leaf_id, eth_num, ip_address, **args):
    """Relation that defines which leaf path endpoints (ports and port channels) will be used to reach the external layer 3 network. The corresponding set of policies will be resolved into the specified leaf path endpoints. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    l3ext_rspathl3outatt = RsPathL3OutAtt(l3ext_lifp,
                                          'topology/pod-1/paths-' + leaf_id + '/pathep-[eth' + eth_num + ']',
                                          addr=ip_address,
                                          ifInstT='12',
                                          mtu=get_value(args, 'mtu', 'inherit'),
                                          targetDscp=get_value(args, 'target_dscp', 'unspecified'))
    ospf_ifp = IfP(l3ext_lifp)


class CreateRoutedInterfaceProfile(CreateMo):

    def __init__(self):
        self.description = 'Relation that defines which leaf path endpoints (ports and port channels) will be used to reach the external layer 3 network. The corresponding set of policies will be resolved into the specified leaf path endpoints. '
        self.tenant_required = True
        self.routed_outside = None
        self.node_profile = None
        self.interface_profile = None
        self.leaf_id = None
        self.eth_num = None
        self.ip_address = None
        super(CreateRoutedInterfaceProfile, self).__init__()

    def set_cli_mode(self):
        super(CreateRoutedInterfaceProfile, self).set_cli_mode()
        self.parser_cli.add_argument('routed_outside', help='The name for the policy controlling connectivity to the outside.')
        self.parser_cli.add_argument('node_profile', help='The name of the logical node profile.')
        self.parser_cli.add_argument('interface_profile', help='The name of the logical interface profile.')
        self.parser_cli.add_argument('leaf_id', help='Leaf ID.')
        self.parser_cli.add_argument('eth_num', help='Eth Number.')
        if not self.delete:
            self.parser_cli.add_argument('ip_address', help='The IP address of the path attached to the layer 3 outside profile.')
        self.parser_cli.add_argument('-M', '--MTU', dest='mtu', help='The maximum transmit unit of the external network.')
        self.parser_cli.add_argument('-D', '--target_DSCP', dest='target_dscp', help='The target differentiated services code point (DSCP) of the path attached to the layer 3 outside profile.')

    def read_key_args(self):
        self.routed_outside = self.args.pop('routed_outside')
        self.node_profile = self.args.pop('node_profile')
        self.interface_profile = self.args.pop('interface_profile')
        self.leaf_id = str(self.args.pop('leaf_id'))
        self.eth_num = str(self.args.pop('eth_num'))
        self.ip_address = self.args.pop('ip_address')

    def wizard_mode_input_args(self):
        self.args['routed_outside'] = input_routed_outside(msg='\nPlease specify the Routed Interface Profile: ')
        self.args['node_profile'] = input_node_profile('')
        self.args['interface_profile'] = input_interface_profile('')
        self.args['leaf_id'], self.args['eth_num'], self.args['ip_address'] = input_key_args('', delete_function=self.delete)

        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/lnodep-' + self.node_profile + '/lifp-' + self.interface_profile + '/rspathL3OutAtt-[topology/pod-1/paths-' + self.leaf_id + '/pathep-[eth' + self.eth_num + ']]', module=RsPathL3OutAtt, description='Routed Interface Profile')
        super(CreateRoutedInterfaceProfile, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.check_if_tenant_exist()
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-', self.routed_outside, Out, description='The policy')
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/lnodep-', self.node_profile, LNodeP, description='Node Profile')
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/lnodep-' + self.node_profile + '/lifp-', self.interface_profile, LIfP, description='Interface Profile')
        create_routed_interface_profile(self.mo, self.leaf_id, self.eth_num, self.ip_address, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateRoutedInterfaceProfile()