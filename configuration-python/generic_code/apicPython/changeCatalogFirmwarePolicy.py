from cobra.model.firmware import CatFwP

from createMo import *


def input_key_args(msg='\nPlease Target Firmware Version:'):
    print msg
    return input_raw_input("Target Firmware Version", required=True)


def change_catalog_firmware_policy(parent_mo, target_firmware_policy):
    """change catalog firmware policy"""
    firmware_catfwp = CatFwP(parent_mo, version=target_firmware_policy)


class ChangeCatalogFirmwarePolicy(CreateMo):

    def __init__(self):
        self.description = 'change catalog firmware policy'
        self.target_firmware_policy = None
        super(ChangeCatalogFirmwarePolicy, self).__init__()

    def set_cli_mode(self):
        super(ChangeCatalogFirmwarePolicy, self).set_cli_mode()
        self.parser_cli.add_argument('target_firmware_policy', help='Target Firmware Version.')

    def read_key_args(self):
        self.target_firmware_policy = self.args.pop('target_firmware_policy')

    def wizard_mode_input_args(self):
        self.args['target_firmware_policy'] = input_key_args()

    def delete_mo(self):
        print 'Cant be delete'
        sys.exit()

    def main_function(self):
        # Query a parent
        self.look_up_mo('uni/fabric/', '')
        change_catalog_firmware_policy(self.mo, self.target_firmware_policy)


if __name__ == '__main__':
    mo = ChangeCatalogFirmwarePolicy()


