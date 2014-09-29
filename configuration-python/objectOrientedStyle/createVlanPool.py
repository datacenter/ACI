from cobra.model.fvns import VlanInstP, EncapBlk

from createMo import *

VLAN_MODE_CHOICES = ['dynamic', 'static']


def input_key_args(msg='\nPlease specify the VLAN Pool identity:', delete_function=False):
    print msg
    args = [input_raw_input("VLan Name", required=True),
            input_options("Allocation Mode", '', VLAN_MODE_CHOICES,
                          required=True)]
    if not delete_function:
        args.append(input_raw_input("Vlan Range From", required=True))
        args.append(input_raw_input("Vlan Range To", required=True))
    else:
        args.extend([None,None])
    return args


def create_vlan_pool(infra_infra, vlan, allocation_mode, vlan_range_from, vlan_range_to):
    """Create VLAN Pool"""
    fvns_vlaninstp = VlanInstP(infra_infra, vlan, allocation_mode)
    # Set up the VLAN range.
    fvns_encapblk = EncapBlk(fvns_vlaninstp, 'vlan-'+str(vlan_range_from), 'vlan-'+str(vlan_range_to))


class CreateVlanPool(CreateMo):

    def __init__(self):
        self.description = 'Create VLAN Pool'
        self.vlan_name = None
        self.vlan_mode = None
        self.range_from = None
        self.range_to = None
        super(CreateVlanPool, self).__init__()

    def set_cli_mode(self):
        super(CreateVlanPool, self).set_cli_mode()
        self.parser_cli.add_argument('vlan_name', help='VLAN Pool Name')
        self.parser_cli.add_argument('vlan_mode', help='Allocation Mode', choices=VLAN_MODE_CHOICES)
        self.parser_cli.add_argument('range_from', help='VLAN range from')
        self.parser_cli.add_argument('range_to', help='VLAN range to')

    def read_key_args(self):
        self.vlan_name = self.args.pop('vlan_name')
        self.vlan_mode = self.args.pop('vlan_mode')
        self.range_from = self.args.pop('range_from')
        self.range_to = self.args.pop('range_to')

    def wizard_mode_input_args(self):
        self.args['vlan_name'], self.args['vlan_mode'], self.args['range_from'], self.args['range_to'] = input_key_args(delete_function=self.delete)

    def delete_mo(self):
        self.check_if_mo_exist('uni/infra/vlanns-' + self.vlan_name + '-' + self.vlan_mode, '', VlanInstP, description='VLAN Pool')
        super(CreateVlanPool, self).delete_mo()

    def main_function(self):
        self.look_up_mo('uni/infra','')
        create_vlan_pool(self.mo, self.vlan_name, self.vlan_mode, self.range_from, self.range_to)

if __name__ == '__main__':
    vlan = CreateVlanPool()