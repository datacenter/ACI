from cobra.model.l3ext import Out, LNodeP
from createRoutedOutside import input_key_args as input_routed_outside
from createMo import *

DEFAULT_TARGET_DSCP = 'unspecified'


def input_key_args(msg='\nPlease Specify Node Profile:'):
    print msg
    return input_raw_input("Node Profile Name", required=True)


def input_optional_args():
    args = {'target_dscp': input_options('Target DSCP', DEFAULT_TARGET_DSCP, [])}
    return args


def create_node_profile(l3ext_out, node_profile_name, **args):
    """Create a Node Profile"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    l3ext_lnodep = LNodeP(l3ext_out, node_profile_name,
                          targetDscp=get_value(args, 'target_dscp', DEFAULT_TARGET_DSCP))


class CreateNodeProfile(CreateMo):

    def __init__(self):
        self.description = 'Create the logical node profile that defines a common configuration that will apply to one or more leaf nodes.'
        self.tenant_required = True
        self.routed_outside = None
        self.node_profile = None
        super(CreateNodeProfile, self).__init__()

    def set_cli_mode(self):
        super(CreateNodeProfile, self).set_cli_mode()
        self.parser_cli.add_argument('routed_outside', help='The name for the policy controlling connectivity to the outside.')
        self.parser_cli.add_argument('node_profile', help='The name of the logical node profile.')
        self.parser_cli.add_argument('-t', '--target_dscp', default= DEFAULT_TARGET_DSCP, help='Node level Dscp value.')

    def read_key_args(self):
        self.routed_outside = self.args.pop('routed_outside')
        self.node_profile = self.args.pop('node_profile')

    def wizard_mode_input_args(self):
        self.args['routed_outside'] = input_routed_outside()
        self.args['node_profile'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/lnodep-', self.node_profile, LNodeP, description='Node Profile')
        super(CreateNodeProfile, self).delete_mo()

    def main_function(self):
        self.check_if_tenant_exist()
        l3ext_out = self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-', self.routed_outside, Out, description='The policy')
        create_node_profile(l3ext_out, self.node_profile, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateNodeProfile()