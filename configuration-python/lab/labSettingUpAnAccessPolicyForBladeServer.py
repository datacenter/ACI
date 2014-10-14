from labScript import *

from apicPython import createLinkLevelPolicy
from apicPython import createCdpInterfacePolicy
from apicPython import createLldpInterfacePolicy
from apicPython import createLacpPolicy
from apicPython import createPcInterfacePolicyGroup
from apicPython import configureInterfacePcAndVpc


class SettingUpAnAccessPolicyForBladeServer(LabScript):

    def __init__(self):
        self.description = 'Setting Up An Access Policy For a Blade Server'
        self.switches = []
        self.switch_profile = None
        self.interface_type = None
        self.interface_selector = None
        self.interface_policy_group = None
        self.interface_ports = []
        self.link_level_policy = {}
        self.cdp_interface_policy = {}
        self.lldp_interface_policy = {}
        self.lacp_policy = {}
        super(SettingUpAnAccessPolicyForBladeServer, self).__init__()

    def run_yaml_mode(self):
        super(SettingUpAnAccessPolicyForBladeServer, self).run_yaml_mode()
        self.switches = self.args['switches']
        self.switch_profile = self.args['switch_profile']
        self.interface_type = self.args['interface_type']
        self.interface_selector = self.args['interface_selector']
        self.interface_policy_group = self.args['interface_policy_group']
        self.interface_ports = self.args['interface_ports']
        self.link_level_policy = self.args['link_level_policy']
        self.cdp_interface_policy = self.args['cdp_interface_policy']
        self.lldp_interface_policy = self.args['lldp_interface_policy']
        self.lacp_policy = self.args['lacp_policy']

    def wizard_mode_input_args(self):
        self.switch_profile, self.switches, self.interface_type, self.interface_ports, self.interface_selector, self.interface_policy_group = configureInterfacePcAndVpc.input_key_args()
        self.link_level_policy['name'] = createLinkLevelPolicy.input_key_args()
        self.link_level_policy['optional_args'] = createLinkLevelPolicy.input_optional_args()
        self.cdp_interface_policy['name'] = createCdpInterfacePolicy.input_key_args()
        self.cdp_interface_policy['optional_args'] = createCdpInterfacePolicy.input_optional_args()
        self.lldp_interface_policy['name'] = createLldpInterfacePolicy.input_key_args()
        self.lldp_interface_policy['optional_args'] = createLldpInterfacePolicy.input_optional_args()
        self.lacp_policy['name'] = createLacpPolicy.input_key_args()
        self.lacp_policy['optional_args'] = createLacpPolicy.input_optional_args()

    def main_function(self):

        # create Link Level Policy, CDP Interface Policy, LLDP Interface Policy and LACP Policy
        self.look_up_mo('uni/infra/', '')
        createLinkLevelPolicy.create_link_level_policy(self.mo, self.link_level_policy['name'], optional_args=return_valid_optional_args(self.link_level_policy))

        createCdpInterfacePolicy.create_cdp_interface_policy(self.mo, self.cdp_interface_policy['name'], optional_args=return_valid_optional_args(self.cdp_interface_policy))

        createLldpInterfacePolicy.create_lldp_interface_policy(self.mo, self.lldp_interface_policy['name'], optional_args=return_valid_optional_args(self.lldp_interface_policy))

        createLacpPolicy.create_lacp_policy(self.mo, self.lacp_policy['name'], optional_args=return_valid_optional_args(self.lacp_policy))

        self.commit_change()

        # create PC Interface Policy Group
        self.look_up_mo('uni/infra/funcprof/', '')
        createPcInterfacePolicyGroup.create_pc_interface_policy_group(self.mo, self.interface_policy_group,
                                                                      optional_args={'link_level': self.link_level_policy['name'],
                                                                                     'cdp': self.cdp_interface_policy['name'],
                                                                                     'lldp': self.lldp_interface_policy['name'],
                                                                                     'lacp': self.lacp_policy['name']})
        self.commit_change()

        # configure PC
        self.look_up_mo('uni/infra', '')
        configureInterfacePcAndVpc.configure_interface_pc_and_vpc(self.mo, self.switch_profile, self.switches, self.interface_type, self.interface_ports, self.interface_selector, self.interface_policy_group)


if __name__ == '__main__':
    mo = SettingUpAnAccessPolicyForBladeServer()