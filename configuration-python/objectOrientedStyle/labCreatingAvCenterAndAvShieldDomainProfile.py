import createVcenterDomain
import createAttachableAccessEntityprofile
import configureInterfacePcAndVpc
import createAccessPortPolicyGroup
import createVlanPool
import createVxlanPool
import createMulticastAddressBlock
import createVcenterCredential
import createVcenterController
import createVshieldController

from createMo import *


class LabCreatingAvCenterAndAvShieldDomainProfile(CreateMo):

    def __init__(self):
        self.description = 'Create a vCenter and a vShield Domain Profile'
        self.vcenter_domain = None
        self.vcenter_provider = None
        self.attachable_entity_profile = {}
        self.configured_interfaces_pc_vpc = {}
        self.vlan = {}
        self.vxlan = {}
        self.multicast = {}
        self.vcenter_credentials = {}
        self.vcenter_controller = {}
        self.vshield_controller = {}
        super(LabCreatingAvCenterAndAvShieldDomainProfile, self).__init__()

    def set_argparse(self):
        super(LabCreatingAvCenterAndAvShieldDomainProfile, self).set_argparse()
        self.parser_cli = self.subparsers.add_parser(
            'cli', help='Not Support.'
        )

    def delete_mo(self):
        print 'Delete method is not supported in this function.'
        sys.exit()

    def set_cli_mode(self):
        pass

    def run_cli_mode(self):
        print 'CLI mode is not supported in this method. Please try Yaml mode.'
        sys.exit()

    def run_yaml_mode(self):
        super(LabCreatingAvCenterAndAvShieldDomainProfile, self).run_yaml_mode()
        self.vcenter_domain = self.args['vcenter_domain']
        self.vcenter_provider = self.args['vcenter_provider']
        self.attachable_entity_profile = self.args['attachable_entity_profile']
        self.configured_interfaces_pc_vpc = self.args['configured_interfaces_pc_vpc']
        self.vlan = self.args['vlan']
        self.vxlan = self.args['vxlan']
        self.multicast = self.args['multicast']
        self.vcenter_credentials = self.args['vcenter_credentials']
        self.vcenter_controller = self.args['vcenter_controller']
        self.vshield_controller = self.args['vshield_controller']

    def read_opt_args(self):
        pass

    def wizard_mode_input_args(self):
        self.vcenter_provider, self.vcenter_domain = createVcenterDomain.input_key_args()
        self.attachable_entity_profile['name'] = createAttachableAccessEntityprofile.input_key_args()
        self.attachable_entity_profile['optional_args'] = createAttachableAccessEntityprofile.input_optional_args()
        self.configured_interfaces_pc_vpc['switch_profile'], self.configured_interfaces_pc_vpc['switches'], self.configured_interfaces_pc_vpc['interface_type'], self.configured_interfaces_pc_vpc['interface_ports'], self.configured_interfaces_pc_vpc['interface_selector'], self.configured_interfaces_pc_vpc['interface_policy_group'] = configureInterfacePcAndVpc.input_key_args()
        self.vlan['vlan_name'], self.vlan['vlan_mode'], self.vlan['range_from'], self.vlan['range_to'] = createVlanPool.input_key_args()
        self.vcenter_credentials['profile'], self.vcenter_credentials['vmm_user'], self.vcenter_credentials['vmm_password'] = createVcenterCredential.input_key_args()
        self.vcenter_controller['name'], self.vcenter_controller['host_or_ip'], self.vcenter_controller['data_center'] = createVcenterController.input_key_args()
        self.vcenter_controller['optional_args'] = createVcenterController.input_optional_args()

    def main_function(self):

        # create Vlan Pool, Vxlan Pool and Multicast address block
        self.look_up_mo('uni/infra','')
        createVlanPool.create_vlan_pool(self.mo, self.vlan['vlan_name'], self.vlan['vlan_mode'], self.vlan['range_from'], self.vlan['range_to'])
        createVxlanPool.create_vxlan_pool(self.mo, self.vxlan['vxlan_name'], self.vxlan['range_from'], self.vxlan['range_to'])
        createMulticastAddressBlock.create_multicast_address_pool(self.mo, self.multicast['name'], self.multicast['ip_range_from'], self.multicast['ip_range_to'])
        self.commit_change()

        # create Access Port Policy Group
        self.look_up_mo('uni/infra/funcprof/', '')
        createAccessPortPolicyGroup.create_access_port_port_policy_group(self.mo, self.configured_interfaces_pc_vpc['interface_policy_group'], optional_args={'entity_profile': self.attachable_entity_profile['name']})
        self.commit_change()

        # configure Interface PC and VPC
        self.look_up_mo('uni/infra', '')
        configureInterfacePcAndVpc.configure_interface_pc_and_vpc(self.mo, self.configured_interfaces_pc_vpc['switch_profile'], self.configured_interfaces_pc_vpc['switches'], self.configured_interfaces_pc_vpc['interface_type'], self.configured_interfaces_pc_vpc['interface_ports'], self.configured_interfaces_pc_vpc['interface_selector'], self.configured_interfaces_pc_vpc['interface_policy_group'])

        # create Attachable Access Entity profile
        createAttachableAccessEntityprofile.create_attachable_access_entity_profile(self.mo, self.attachable_entity_profile['name'], optional_args=self.attachable_entity_profile['optional_args'])
        self.commit_change()

        # create vCenter Domain
        self.check_if_mo_exist('uni/vmmp-' + self.vcenter_provider)
        vmm_domp = createVcenterDomain.create_vcenter_domain(self.mo, self.vcenter_domain, optional_args={'vlan': self.vlan['vlan_name'], 'vlan_mode': self.vlan['vlan_mode']})
        self.commit_change()

        # create Vcenter Credentials
        for credential in self.vcenter_credentials:
            createVcenterCredential.create_vcenter_credential(vmm_domp, credential['profile'], credential['vmm_user'], credential['vmm_password'])

        # create vCenter/vShield controller
        vmm_ctrlrp = createVcenterController.create_vcenter_controller(vmm_domp, self.vcenter_controller['name'], self.vcenter_controller['host_or_ip'], self.vcenter_controller['data_center'], optional_args=self.vcenter_controller['optional_args'])
        vmm_usraccp_path = 'uni/vmmp-' + self.vcenter_provider + '/dom-' + self.vcenter_domain + '/usracc-' + self.vcenter_controller['optional_args']['associated_credential']
        createVcenterController.define_associated_credential(vmm_ctrlrp, vmm_usraccp_path)
        vmm_ctrlrp = createVshieldController.create_vshieldr_controller(vmm_domp, self.vcenter_provider, self.vcenter_domain, self.vshield_controller['name'], self.vshield_controller['host_or_ip'], optional_args=self.vshield_controller['optional_args'])
        if is_valid_key(self.vshield_controller['optional_args'], 'associated_credential'):
            vmm_usraccp_path = 'uni/vmmp-' + self.vcenter_provider + '/dom-' + self.vcenter_domain + '/usracc-' + self.vshield_controller['optional_args']['associated_credential']
            createVshieldController.define_associated_credential(vmm_ctrlrp, vmm_usraccp_path)


if __name__ == '__main__':
    mo = LabCreatingAvCenterAndAvShieldDomainProfile()