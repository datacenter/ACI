from cobra.model.ip import RouteP, NexthopP

from createRoutedOutside import input_key_args as input_routed_outside
from createNodesAndInterfacesProfile import input_key_args as input_node_profile
from createNodes import input_key_args as input_leaf_id
from createMo import *


def input_key_args(msg='\nPlease Specify the Static Route:'):
    print msg
    return input_raw_input("Prefix", required=True)


def input_next_hop_address():
    return input_raw_input('Next Hop Address', required=True)


def input_optional_args():
    return {'next_hop_address': read_add_mos_args(add_mos('Add a Next Hop Address', input_next_hop_address))}


def create_static_route(parent_mo, prefix, **args):
    """Create a Static Route that Configure the IP address and next hop IP address for the routed outside network."""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    ip_routep = RouteP(parent_mo, prefix)

    if is_valid_key(args, 'next_hop_address'):
        for ip in args['next_hop_address']:
            ip_nexthopp = NexthopP(ip_routep, ip)


class CreateStaticRoute(CreateMo):

    def __init__(self):
        self.description = 'Create a Static Route that Configure the IP address and next hop IP address for the routed outside network.'
        self.tenant_required = True
        self.tenant = 'mgmt'
        self.routed_outside = None
        self.node_profile = None
        self.leaf_id = None
        self.prefix = None
        super(CreateStaticRoute, self).__init__()

    def set_cli_mode(self):
        super(CreateStaticRoute, self).set_cli_mode()
        self.parser_cli.add_argument('routed_outside', help='The name for the policy controlling connectivity to the outside.')
        self.parser_cli.add_argument('node_profile', help='The name of the logical node profile.')
        self.parser_cli.add_argument('leaf_id', help='Leaf ID')
        self.parser_cli.add_argument('prefix', help='The static route IP address assigned to the outside network.')
        self.parser_cli.add_argument('-n', '--next_hop_address', nargs='+', help='The Nexthop policy for the static route.')

    def read_key_args(self):
        self.routed_outside = self.args.pop('routed_outside')
        self.node_profile = self.args.pop('node_profile')
        self.leaf_id = str(self.args.pop('leaf_id'))
        self.prefix = self.args.pop('prefix')

    def wizard_mode_input_args(self):
        self.args['routed_outside'] = input_routed_outside()
        self.args['node_profile'] = input_node_profile()
        self.args['leaf_id'] = input_leaf_id(delete_function=True)[0]
        self.args['prefix'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-mgmt/out-'+self.routed_outside+'/lnodep-'+self.node_profile+'/rsnodeL3OutAtt-[topology/pod-1/node-'+str(self.leaf_id)+']/rt-['+self.prefix+']', '', RouteP, description='Static Route')
        super(CreateStaticRoute, self).delete_mo()

    def main_function(self):
        # Query to parent
        self.check_if_tenant_exist()
        self.check_if_mo_exist('uni/tn-mgmt/out-'+self.routed_outside+'/lnodep-'+self.node_profile+'/rsnodeL3OutAtt-[topology/pod-1/node-'+str(self.leaf_id)+']')
        create_static_route(self.mo, self.prefix, optional_args=self.optional_args)


if __name__ == '__main__':
    mo = CreateStaticRoute()


