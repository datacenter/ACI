from cobra.model.fvns import McastAddrInstP, McastAddrBlk

from createMo import *


def input_key_args(msg='\nPlease specify the Multicast Address Pool identity:', delete_function=False):
    print msg
    args = [input_raw_input("Multicast Address Pool Name", required=True)]
    if not delete_function:
        args.append(input_raw_input("IP Range From", required=True))
        args.append(input_raw_input("IP Range To", required=True))
    else:
        args.extend([None,None])
    return args


def create_multicast_address_pool(infra_infra, multicast, ip_range_from, ip_range_to):
    """Create Multicast Address Pool. The policy definition of the multicast IP address ranges. These addresses can be used for various purposes, such as VxLAN encapsulation. """
    fvns_mcastaddrinstp = McastAddrInstP(infra_infra, multicast)
    # Set up the Multicast Address Pool range.
    fvns_encapblk = McastAddrBlk(fvns_mcastaddrinstp, ip_range_from, ip_range_to)


class CreateMulticastAddressPool(CreateMo):

    def __init__(self):
        self.description = 'Create Multicast Address Pool. The policy definition of the multicast IP address ranges. These addresses can be used for various purposes, such as VxLAN encapsulation. '
        self.multicast = None
        self.ip_range_from = None
        self.ip_range_to = None
        super(CreateMulticastAddressPool, self).__init__()

    def set_cli_mode(self):
        super(CreateMulticastAddressPool, self).set_cli_mode()
        self.parser_cli.add_argument('multicast', help='Multicast Address Pool Name')
        self.parser_cli.add_argument('ip_range_from', help='Multicast Address Pool range from')
        self.parser_cli.add_argument('ip_range_to', help='Multicast Address Pool range to')

    def read_key_args(self):
        self.multicast = self.args.pop('multicast')
        self.ip_range_from = self.args.pop('ip_range_from')
        self.ip_range_to = self.args.pop('ip_range_to')

    def wizard_mode_input_args(self):
        self.args['multicast'], self.args['ip_range_from'], self.args['ip_range_to'] = input_key_args(delete_function=self.delete)

    def delete_mo(self):
        self.check_if_mo_exist('uni/infra/maddrns-', self.multicast, McastAddrInstP, description='Multicast Address Pool')
        super(CreateMulticastAddressPool, self).delete_mo()

    def main_function(self):
        self.look_up_mo('uni/infra', '')
        create_multicast_address_pool(self.mo, self.multicast, self.ip_range_from, self.ip_range_to)

if __name__ == '__main__':
    Multicast = CreateMulticastAddressPool()