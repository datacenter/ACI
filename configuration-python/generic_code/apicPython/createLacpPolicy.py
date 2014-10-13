from cobra.model.lacp import LagPol

from createMo import *

DEFAULT_MINIMUM_LINKS = 1
DEFAULT_MAXIMUM_LINKS = 16
DEFAULT_YES = 'yes'
DEFAULT_NO = 'no'

MODE_CHOICES = ['off', 'active', 'passive', 'mac-pin']
CONTROL_CHOICES = ['yes', 'no']


def input_key_args(msg='\nPlease Specify LACP Policy:'):
    print msg
    return input_raw_input("LACP Policy Name", required=True)


def input_optional_args():

    args = {}
    args['mode'] = input_options('Mode', MODE_CHOICES[0], MODE_CHOICES)

    if args['mode'] == 'active' or args['mode'] == 'passive':

        args['control'] = []

        def apply_control(control, prompt, default=DEFAULT_YES):
            if input_yes_no(prompt, default=default):
                args['control'].append(control)

        apply_control('graceful-conv', 'Apply Graceful Convergence', default=DEFAULT_YES)
        apply_control('susp-individual', 'Suspend Individual Port', default=DEFAULT_YES)
        apply_control('load-defer', 'Load Defer Member Ports', default=DEFAULT_NO)
        apply_control('fast-sel-hot-stdby', 'Fast Select Hot Standby Ports', default=DEFAULT_YES)

    args['minimum_number_of_links'] = input_options('Minimum Number of Links', str(DEFAULT_MINIMUM_LINKS), '', num_accept=True)
    args['maximum_number_of_links'] = input_options('Maximum Number of Links', str(DEFAULT_MAXIMUM_LINKS), '', num_accept=True)
    return args


def create_lacp_policy(parent_mo, lacp_policy, **args):
    """Create LACP Policy"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    # Create mo
    args['mode'] = get_value(args, 'mode', MODE_CHOICES[0])
    if args['mode'] not in ['active', 'passive']:
        args['control'] = ''
    lacp_lagpol = LagPol(parent_mo, lacp_policy,
                         mode=get_value(args, 'mode', MODE_CHOICES[0]),
                         minLinks=get_value(args, 'minimum_number_of_links', DEFAULT_MINIMUM_LINKS),
                         maxLinks=get_value(args, 'maximum_number_of_links', DEFAULT_MAXIMUM_LINKS),
                         ctrl=(',').join(args['control']))
    return lacp_lagpol


class CreateLacpPolicy(CreateMo):

    def __init__(self):
        self.description = 'Create LACP Policy. LACP enables you to bundle several physical ports together to form a single port channel. LACP enables a node to negotiate an automatic bundling of links by sending LACP packets to the peer node.'
        self.lacp_policy = None
        super(CreateLacpPolicy, self).__init__()

    def set_cli_mode(self):
        super(CreateLacpPolicy, self).set_cli_mode()
        self.parser_cli.add_argument('lacp_policy', help='The name of the policy. ')
        self.parser_cli.add_argument('-m', '--mode', default= MODE_CHOICES[0], choices=MODE_CHOICES, help='Mode')
        self.parser_cli.add_argument('-i', '--minimum_number_of_links', default= DEFAULT_MINIMUM_LINKS, help='MinLinks in the port channel')
        self.parser_cli.add_argument('-a', '--maximum_number_of_links', default= DEFAULT_MAXIMUM_LINKS, help='Maxinmum links')
        self.parser_cli.add_argument('-g', dest='graceful_convergence', action='store_const', const=True, default= False, help='LACP graceful convergence')
        self.parser_cli.add_argument('-s', dest='suspend_individual_port', action='store_const', const=True, default= False, help='LACP suspend individual port')
        self.parser_cli.add_argument('-l', dest='load_defer_member_ports', action='store_const', const=True, default= False, help='Load defer')
        self.parser_cli.add_argument('-f', dest='fast_select_hot_standby_ports', action='store_const', const=True, default= False, help='LACP fast select for hot standby ports')

    def read_key_args(self):
        self.lacp_policy = self.args.pop('lacp_policy')

    def wizard_mode_input_args(self):
        self.args['lacp_policy'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def run_cli_mode(self):
        super(CreateLacpPolicy, self).run_cli_mode()
        self.args['control'] = []
        if self.args['graceful_convergence']:
            self.args['control'].append('graceful-conv')
        if self.args['suspend_individual_port']:
            self.args['control'].append('susp-individual')
        if self.args['load_defer_member_ports']:
            self.args['control'].append('load-defer')
        if self.args['fast_select_hot_standby_ports']:
            self.args['control'].append('fast-sel-hot-stdby')

    def delete_mo(self):
        self.check_if_mo_exist('uni/infra/lacplagp-', self.lacp_policy, LagPol, description='LACP Policy')
        super(CreateLacpPolicy, self).delete_mo()

    def main_function(self):
        # Query to parent
        self.look_up_mo('uni/infra/', '')
        create_lacp_policy(self.mo, self.lacp_policy, optional_args=self.optional_args)


if __name__ == '__main__':
    mo = CreateLacpPolicy()


