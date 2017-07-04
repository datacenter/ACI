from labScript import *

from apicPython import createOutsideFirmwareSource
from apicPython import upgradeControllerFirmwarePolicy


class UpgradingTheApicControllerSoftwareVersion(LabScript):

    def __init__(self):
        self.description = 'Upgrading the APIC Controller Software Version.'
        self.firmware_source = {}
        self.upgrade_controller_firmware_policy = {}
        super(UpgradingTheApicControllerSoftwareVersion, self).__init__()

    def run_yaml_mode(self):
        super(UpgradingTheApicControllerSoftwareVersion, self).run_yaml_mode()
        self.firmware_source = self.args['firmware_source']
        self.upgrade_controller_firmware_policy = self.args['upgrade_controller_firmware_policy']

    def wizard_mode_input_args(self):
        self.firmware_source['name'] = createOutsideFirmwareSource.input_key_args()
        self.firmware_source['optional_args'] = createOutsideFirmwareSource.input_optional_args()
        self.upgrade_controller_firmware_policy = upgradeControllerFirmwarePolicy.input_optional_args()

    def main_function(self):

        # create Outside Firmware Source
        self.look_up_mo('uni/fabric/fwrepop', '')
        createOutsideFirmwareSource.create_outside_firmware_source(self.mo, self.firmware_source['name'], optional_args=return_valid_optional_args(self.firmware_source))
        self.commit_change()

        # upgrade controller firmware policy
        self.look_up_mo('uni/controller', '')
        upgradeControllerFirmwarePolicy.upgrade_controller_firmware_policy(self.mo, optional_args=self.upgrade_controller_firmware_policy)
        

if __name__ == '__main__':
    mo = UpgradingTheApicControllerSoftwareVersion()