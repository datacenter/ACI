from cobra.model.lldp import IfPol

from createMo import *

DEFAULT_STATE = 'enabled'

STATE_CHOICES = ['enabled', 'disabled']


def input_key_args(msg='\nPlease Specify LLDP Interface Policy:'):
    print msg
    return input_raw_input("LLDP Interface Policy Name", required=True)


def input_optional_args():
    args = {}
    args['receive_state'] = input_options('Receive State', DEFAULT_STATE, STATE_CHOICES)
    args['transmit_state'] = input_options('Transmit State', DEFAULT_STATE, STATE_CHOICES)
    return args


def create_lldp_interface_policy(parent_mo, lldp_interface_policy, **args):
    """Create LLDP Interface Policy"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    # Create mo

    lldp_ifpol = IfPol(parent_mo, lldp_interface_policy,
                       adminRxSt=get_value(args, 'receive_state', DEFAULT_STATE),
                       adminTxSt=get_value(args, 'transmit_state', DEFAULT_STATE))

    return lldp_ifpol


class CreateLldpInterfacePolicy(CreateMo):

    def __init__(self):
        self.description = 'Create LLDP Interface Policy. The LLDP policy parameters for the interface. LLDP uses the logical link control (LLC) services to transmit and receive information to and from other LLDP agents.'
        self.lldp_interface_policy = None
        super(CreateLldpInterfacePolicy, self).__init__()

    def set_cli_mode(self):
        super(CreateLldpInterfacePolicy, self).set_cli_mode()
        self.parser_cli.add_argument('lldp_interface_policy', help='LLDP interface policy name.')
        self.parser_cli.add_argument('-r', '--receive_state', default= DEFAULT_STATE, choices=STATE_CHOICES, help='Receive admin state')
        self.parser_cli.add_argument('-t', '--transmit_state', default= DEFAULT_STATE, choices=STATE_CHOICES, help='Transmit admin state')

    def read_key_args(self):
        self.lldp_interface_policy = self.args.pop('lldp_interface_policy')

    def wizard_mode_input_args(self):
        self.args['lldp_interface_policy'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/infra/lldpIfP-', self.lldp_interface_policy, IfPol, description='LLDP Interface Policy')
        super(CreateLldpInterfacePolicy, self).delete_mo()

    def main_function(self):
        # Query to parent
        self.look_up_mo('uni/infra/', '')
        create_lldp_interface_policy(self.mo, self.lldp_interface_policy, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateLldpInterfacePolicy()




