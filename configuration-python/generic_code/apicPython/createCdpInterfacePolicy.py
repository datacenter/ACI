from cobra.model.cdp import IfPol

from createMo import *

DEFAULT_ADMIN_STATE = 'enabled'

ADMIN_STATE_CHOICES = ['enabled', 'disabled']


def input_key_args(msg='\nPlease Specify CDP Interface Policy:'):
    print msg
    return input_raw_input("CDP Interface Policy Name", required=True)


def input_optional_args():
    args = {}
    args['admin_state'] = input_options('Admin State', DEFAULT_ADMIN_STATE, ADMIN_STATE_CHOICES)
    return args


def create_cdp_interface_policy(parent_mo, cdp_interface_policy, **args):
    """Create CDP Interface Policy"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    # Create mo

    cdp_ifpol = IfPol(parent_mo, cdp_interface_policy,
                         adminSt=get_value(args, 'admin_state', DEFAULT_ADMIN_STATE))

    return cdp_ifpol


class CreateCdpInterfacePolicy(CreateMo):

    def __init__(self):
        self.description = 'Create CDP Interface Policy. Configure CDP Interface Policy parameters. CDP is primarily used to obtain protocol addresses of neighboring devices and discover the platform of those devices. CDP can also be used to display information about the interfaces your router uses. CDP is media- and protocol-independent, and runs on all Cisco-manufactured equipment including routers, bridges, access servers, and switches.'
        self.cdp_interface_policy = None
        super(CreateCdpInterfacePolicy, self).__init__()

    def set_cli_mode(self):
        super(CreateCdpInterfacePolicy, self).set_cli_mode()
        self.parser_cli.add_argument('cdp_interface_policy', help='CDP Interface Policy Name. ')
        self.parser_cli.add_argument('-a', '--admin_state', default= DEFAULT_ADMIN_STATE, choices=ADMIN_STATE_CHOICES, help='Admin state')

    def read_key_args(self):
        self.cdp_interface_policy = self.args.pop('cdp_interface_policy')

    def wizard_mode_input_args(self):
        self.args['cdp_interface_policy'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/infra/cdpIfP-', self.cdp_interface_policy, IfPol, description='CDP Interface Policy')
        super(CreateCdpInterfacePolicy, self).delete_mo()

    def main_function(self):
        # Query to parent
        self.look_up_mo('uni/infra/', '')
        create_cdp_interface_policy(self.mo, self.cdp_interface_policy, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateCdpInterfacePolicy()




