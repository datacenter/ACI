from cobra.model.fvns import VxlanInstP, EncapBlk

from createMo import *


def input_key_args(msg='\nPlease specify the VXLAN Pool identity:', delete_function=False):
    print msg
    args = [input_raw_input("VXLAN Name", required=True)]
    if not delete_function:
        args.append(input_raw_input("VXLAN Range From (start from 5000)", required=True))
        args.append(input_raw_input("VXLAN Range To", required=True))
    else:
        args.extend([None,None])
    return args


def create_vxlan_pool(infra_infra, vxlan, vxlan_range_from, vxlan_range_to):
    """Create VXLAN Pool"""
    fvns_vxlaninstp = VxlanInstP(infra_infra, vxlan)
    # Set up the VXLAN range.
    fvns_encapblk = EncapBlk(fvns_vxlaninstp, 'vxlan-'+str(vxlan_range_from), 'vxlan-'+str(vxlan_range_to))


class CreateVxlanPool(CreateMo):

    def __init__(self):
        self.description = 'Create VXLAN Pool'
        self.vxlan_name = None
        self.range_from = None
        self.range_to = None
        super(CreateVxlanPool, self).__init__()

    def set_cli_mode(self):
        super(CreateVxlanPool, self).set_cli_mode()
        self.parser_cli.add_argument('vxlan_name', help='VXLAN Pool Name')
        self.parser_cli.add_argument('range_from', help='VXLAN range from')
        self.parser_cli.add_argument('range_to', help='VXLAN range to')

    def read_key_args(self):
        self.vxlan_name = self.args.pop('vxlan_name')
        self.range_from = self.args.pop('range_from')
        self.range_to = self.args.pop('range_to')

    def wizard_mode_input_args(self):
        self.args['vxlan_name'], self.args['range_from'], self.args['range_to'] = input_key_args(delete_function=self.delete)

    def delete_mo(self):
        self.check_if_mo_exist('uni/infra/vxlanns-', self.vxlan_name, VxlanInstP, description='VXLAN Pool')
        super(CreateVxlanPool, self).delete_mo()

    def main_function(self):
        self.look_up_mo('uni/infra','')
        create_vxlan_pool(self.mo, self.vxlan_name, str(self.range_from), str(self.range_to))

if __name__ == '__main__':
    vxlan = CreateVxlanPool()