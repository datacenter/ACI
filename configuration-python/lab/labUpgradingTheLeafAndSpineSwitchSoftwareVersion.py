from labScript import *

from apicPython import createOutsideFirmwareSource
from apicPython import createFirmwareGroup
from apicPython import createMaintenanceGroup


class UpgradingTheLeafAndSpineSwitchSoftwareVersion(LabScript):

    def __init__(self):
        self.description = 'Upgrading the Leaf and Spine Switch Software Version.'
        self.firmware_source = {}
        self.firmware_group = {}
        self.maintenance_group = {}
        super(UpgradingTheLeafAndSpineSwitchSoftwareVersion, self).__init__()

    def run_yaml_mode(self):
        super(UpgradingTheLeafAndSpineSwitchSoftwareVersion, self).run_yaml_mode()
        self.firmware_source = self.args['firmware_source']
        self.firmware_group = self.args['firmware_group']
        self.maintenance_group = self.args['maintenance_group']

    def wizard_mode_input_args(self):
        self.firmware_source['name'] = createOutsideFirmwareSource.input_key_args()
        self.firmware_source['optional_args'] = createOutsideFirmwareSource.input_optional_args()
        self.firmware_group['name'] = createFirmwareGroup.input_key_args()
        self.firmware_group['optional_args'] = createFirmwareGroup.input_optional_args()
        self.maintenance_group['name'] = createMaintenanceGroup.input_key_args()
        self.maintenance_group['optional_args'] = createMaintenanceGroup.input_optional_args()

    def main_function(self):

        # create Outside Firmware Source
        self.look_up_mo('uni/fabric/fwrepop', '')
        createOutsideFirmwareSource.create_outside_firmware_source(self.mo, self.firmware_source['name'], optional_args=return_valid_optional_args(self.firmware_source))
        self.commit_change()

        # create Firmware Group and Maintenance Group
        self.look_up_mo('uni/fabric', '')
        createFirmwareGroup.create_firmware_group(self.mo, self.firmware_group['name'], optional_args=return_valid_optional_args(self.firmware_group))
        createMaintenanceGroup.create_maintenance_group(self.mo, self.maintenance_group['name'], optional_args=return_valid_optional_args(self.maintenance_group))


if __name__ == '__main__':
    mo = UpgradingTheLeafAndSpineSwitchSoftwareVersion()