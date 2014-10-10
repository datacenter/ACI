from cobra.model.fabric import HIfPol

from createMo import *

DEFAULT_AUTO_NEGOTIATION = 'on'
DEFAULT_SPEED = '10G'
DEFAULT_LINK_DEBOUNCE_INTERVAL = 100

AUTO_NEGOTIATION_CHOICES = ['on', 'off']
SPEED_CHOICES = ['100M', '1G', '10G', '40G']


def input_key_args(msg='\nPlease Specify Link Level Policy:'):
    print msg
    return input_raw_input("Link Level Policy Name", required=True)


def input_optional_args():
    args = {}
    args['atuo_negotiation'] = input_options('Auto Negotiation', DEFAULT_AUTO_NEGOTIATION, AUTO_NEGOTIATION_CHOICES)
    args['speed'] = input_options('Speed', DEFAULT_SPEED, SPEED_CHOICES)
    args['link_debounce_interval'] = input_options('Link Debounce Interval (msec)', str(DEFAULT_LINK_DEBOUNCE_INTERVAL), '', num_accept=True)
    return args


def create_link_level_policy(parent_mo, link_level_policy, **args):
    """Create Link Level Policy"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    # Create mo

    if is_valid_key(args, 'atuo_negotiation'):
        if args['atuo_negotiation'] or args['atuo_negotiation'] == 'on':
            args['atuo_negotiation'] = 'on'
        elif not args['atuo_negotiation'] or args['atuo_negotiation'] == 'off':
            args['atuo_negotiation'] = 'off'

    fabric_hifpol = HIfPol(parent_mo, link_level_policy,
                           autoNeg=get_value(args, 'atuo_negotiation', DEFAULT_AUTO_NEGOTIATION),
                           speed=get_value(args, 'speed', DEFAULT_SPEED),
                           linkDebounce=get_value(args, 'link_debounce_interval', DEFAULT_LINK_DEBOUNCE_INTERVAL),
                           )
    return fabric_hifpol


class CreateLinkLevelPolicy(CreateMo):

    def __init__(self):
        self.description = 'Create Link Level Policy. The host interface policy. This specifies the layer 1 parameters of host facing ports. '
        self.link_level_policy = None
        super(CreateLinkLevelPolicy, self).__init__()

    def set_cli_mode(self):
        super(CreateLinkLevelPolicy, self).set_cli_mode()
        self.parser_cli.add_argument('link_level_policy', help='The name of the interface policy. ')
        self.parser_cli.add_argument('-a', '--atuo_negotiation', default= DEFAULT_AUTO_NEGOTIATION, choices=AUTO_NEGOTIATION_CHOICES, help='The policy auto-negotiation. Auto-negotiation is an optional function of the IEEE 802.3u Fast Ethernet standard that enables devices to automatically exchange information over a link about speed and duplex abilities.')
        self.parser_cli.add_argument('-s', '--speed', default= DEFAULT_SPEED, choices=SPEED_CHOICES, help='The interface policy administrative port speed. The data transfer rate for the port should match the destination to which the port is linked. The administrative speed can be changed only for certain ports, and not all speeds are available on all systems. For more information, see the Hardware Installation Guide for your fabric interconnect.')
        self.parser_cli.add_argument('-l', '--link_debounce_interval', default= DEFAULT_LINK_DEBOUNCE_INTERVAL, help='The interface policy administrative port link debounce interval. Enables the debounce timer for physical interface ports and sets it for a specified amount of time in milliseconds. The debounce timer is disabled if you specify the time to 0 ms.')

    def read_key_args(self):
        self.link_level_policy = self.args.pop('link_level_policy')

    def wizard_mode_input_args(self):
        self.args['link_level_policy'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/infra/hintfpol-', self.link_level_policy, HIfPol, description='Link Level Policy')
        super(CreateLinkLevelPolicy, self).delete_mo()

    def main_function(self):
        # Query to parent
        self.look_up_mo('uni/infra/', '')
        create_link_level_policy(self.mo, self.link_level_policy, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateLinkLevelPolicy()


