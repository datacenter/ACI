from cobra.model.firmware import CtrlrFwP
from cobra.model.maint import CtrlrMaintP
from cobra.model.trig import SchedP

from createMo import *


DEFAULT_IGNORE_COMPATIBILITY = 'false'

IGNORE_COMPATIBILITY_CHOICES = ['true', 'false']


def input_optional_args():
    args = {}
    args['ignore_compatibility'] = input_options('Ignore Compatibility', DEFAULT_IGNORE_COMPATIBILITY, IGNORE_COMPATIBILITY_CHOICES)
    args['target_firmware_version'] = input_raw_input('Target Firmware Version')
    return args


def upgrade_controller_firmware_policy(parent_mo, **args):
    """Upgrade Controller Firmware Policy"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    firmware_ctrlrfwp = CtrlrFwP(parent_mo,
                                 version=get_value(args, 'target_firmware_version', ''),
                                 ignoreCompat = get_value(args, 'ignore_compatibility', DEFAULT_IGNORE_COMPATIBILITY))
    maint_ctrlrmaintp = CtrlrMaintP(parent_mo)


class UpgradeControllerFirmwarePolicy(CreateMo):

    def __init__(self):
        self.description = 'Upgrade Controller Firmware Policy'
        super(UpgradeControllerFirmwarePolicy, self).__init__()

    def set_cli_mode(self):
        super(UpgradeControllerFirmwarePolicy, self).set_cli_mode()
        self.parser_cli.add_argument('-v', '--target_firmware_version', help='The firmware version.')
        self.parser_cli.add_argument('-c', '--ignore_compatibility', default= DEFAULT_IGNORE_COMPATIBILITY, choices=IGNORE_COMPATIBILITY_CHOICES, help='A property for specifying whether compatibility checks should be ignored when applying the firmware policy.')

    def read_key_args(self):
        pass

    def wizard_mode_input_args(self):
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        print 'Reset.'
        self.look_up_mo('uni/controller', '')
        self.optional_args={'ignore_compatibility': DEFAULT_IGNORE_COMPATIBILITY,
                            'target_firmware_version': ''}
        upgrade_controller_firmware_policy(self.mo, optional_args=self.optional_args)


    def main_function(self):
        # Query a parent
        self.look_up_mo('uni/controller', '')
        upgrade_controller_firmware_policy(self.mo, optional_args=self.optional_args)


if __name__ == '__main__':
    mo = UpgradeControllerFirmwarePolicy()


