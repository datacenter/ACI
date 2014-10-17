from cobra.model.firmware import FwGrp, FwP, RsFwgrpp
from cobra.model.fabric import NodeBlk

from createMo import *


DEFAULT_IGNORE_COMPATIBILITY = 'false'

IGNORE_COMPATIBILITY_CHOICES = ['true', 'false']


def input_key_args(msg='\nPlease Specify the Firmware Group:'):
    print msg
    return input_raw_input("Firmware Group Name", required=True)


def input_group_node_id():
    return input_raw_input('Group Node ID', required=True)


def input_optional_args():
    args = {}
    args['ignore_compatibility'] = input_options('Ignore Compatibility', DEFAULT_IGNORE_COMPATIBILITY, IGNORE_COMPATIBILITY_CHOICES)
    args['target_firmware_version'] = input_raw_input('Target Firmware Version')
    args['group_node_ids'] = read_add_mos_args(add_mos('Add a Group Node Id', input_group_node_id))
    return args


def create_firmware_group(parent_mo, firmware_group, **args):
    """create Firmware Group"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    firmware_fwgrp = FwGrp(parent_mo, firmware_group)
    firmware_rsfwgrpp = RsFwgrpp(firmware_fwgrp, tnFirmwareFwPName=firmware_group)
    if is_valid_key(args, 'group_node_ids'):
        for group_node_id in args['group_node_ids']:
            fabric_nodeblk = NodeBlk(firmware_fwgrp, group_node_id)
    firmware_fwp = FwP(parent_mo, firmware_group,
                       version=get_value(args, 'target_firmware_version', ''),
                       ignoreCompat=get_value(args, 'ignore_compatibility', DEFAULT_IGNORE_COMPATIBILITY))


class CreateFirmwareGroup(CreateMo):

    def __init__(self):
        self.description = 'create Firmware Group. This group is a set of nodes to which a firmware policy may be applied. '
        self.firmware_group = None
        super(CreateFirmwareGroup, self).__init__()

    def set_cli_mode(self):
        super(CreateFirmwareGroup, self).set_cli_mode()
        self.parser_cli.add_argument('firmware_group', help='The name for the set of nodes that the firmware version is applied to.')
        self.parser_cli.add_argument('-c', '--ignore_compatibility', default= DEFAULT_IGNORE_COMPATIBILITY, choices=IGNORE_COMPATIBILITY_CHOICES, help='A property for specifying whether compatibility checks should be ignored when applying the firmware policy.')
        self.parser_cli.add_argument('-v', '--target_firmware_version', help='The firmware version.')
        self.parser_cli.add_argument('-g', '--group_node_ids', nargs='+', help='The node block. This is a range of nodes. Each node block begins with the first port and ends with the last port.')

    def read_key_args(self):
        self.firmware_group = self.args.pop('firmware_group')

    def wizard_mode_input_args(self):
        self.args['firmware_group'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/fabric/fwgrp-', self.firmware_group, FwGrp, description='Firmware Group')
        super(CreateFirmwareGroup, self).delete_mo()
        self.commit_change()
        self.check_if_mo_exist('uni/fabric/fwpol-', self.firmware_group, FwP,)
        super(CreateFirmwareGroup, self).delete_mo()

    def main_function(self):
        # Query to parent
        self.look_up_mo('uni/fabric', '')
        create_firmware_group(self.mo, self.firmware_group, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateFirmwareGroup()


