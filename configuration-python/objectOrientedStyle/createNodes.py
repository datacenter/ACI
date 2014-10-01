from createRoutedOutside import input_key_args as input_routed_outside
from createNodesAndInterfacesProfile import input_key_args as input_node_profile
from cobra.model.l3ext import LNodeP, RsNodeL3OutAtt

from createMo import *


def input_key_args(msg='\nPlease Specify Node Profile:', delete_function=False):
    print msg
    key_args = [input_raw_input("Leaf ID", required=True)]
    if not delete_function:
        key_args.append(input_raw_input("Router ID", required=True))
    else:
        key_args.extend([None])
    return key_args


def create_node(l3ext_lnodep, leaf_id, router_id):
    """Create a node"""
    l3ext_rsnodel3outatt = RsNodeL3OutAtt(l3ext_lnodep, 'topology/pod-1/node-' + leaf_id, rtrId=router_id)
    return l3ext_rsnodel3outatt


class CreateNode(CreateMo):

    def __init__(self):
        self.description = 'Represents a static association with each leaf node that is part of the node profile.'
        self.tenant_required = True # (or False)
        self.leaf_id = None
        self.router_id = None
        self.routed_outside = None
        self.node_profile = None
        super(CreateNode, self).__init__()

    def set_cli_mode(self):
        super(CreateNode, self).set_cli_mode()
        self.parser_cli.add_argument('routed_outside', help='The name for the policy controlling connectivity to the outside.')
        self.parser_cli.add_argument('node_profile', help='The name of the logical node profile.')
        self.parser_cli.add_argument('leaf_id', help='Leaf ID')
        self.parser_cli.add_argument('router_id', help='Router ID')

    def read_key_args(self):
        self.routed_outside = self.args.pop('routed_outside')
        self.node_profile = self.args.pop('node_profile')
        self.leaf_id = str(self.args.pop('leaf_id'))
        self.router_id = self.args.pop('router_id')

    def wizard_mode_input_args(self):
        self.args['routed_outside'] = input_routed_outside()
        self.args['node_profile'] = input_node_profile()
        self.args['leaf_id'], self.args['router_id'] = input_key_args(delete_function=self.delete)

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/lnodep-' + self.node_profile + '/rsnodeL3OutAtt-[topology/pod-1/node-' + self.leaf_id + ']', '',  RsNodeL3OutAtt, description='Node')
        super(CreateNode, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.check_if_tenant_exist()
        l3ext_lnodep = self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/lnodep-', self.node_profile, LNodeP, description='Node and Interface Profile')
        create_node(l3ext_lnodep, self.leaf_id, self.router_id)

if __name__ == '__main__':
    mo = CreateNode()