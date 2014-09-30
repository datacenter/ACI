import createNodeManagementAddress
import createOutOfBandContract
import addMgmtProvidedOutOfBandContract
import createExternalManagementEntityInstance

from createMo import *


class LabConfiguringOutOfBandManagementAccess(CreateMo):

    def __init__(self):
        self.description = 'Configuring Out-of-Band Management Access'
        self.tenant_required = True
        self.tenant = 'mgmt'
        self.management_address = {}
        self.out_of_band_contract = {}
        self.out_of_band_epg = {}
        self.external_management_entity_instance = {}
        super(LabConfiguringOutOfBandManagementAccess, self).__init__()

    def set_argparse(self):
        super(LabConfiguringOutOfBandManagementAccess, self).set_argparse()
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
        super(LabConfiguringOutOfBandManagementAccess, self).run_yaml_mode()
        self.management_address = self.args['management_address']
        self.out_of_band_contract = self.args['out_of_band_contract']
        self.out_of_band_epg = self.args['out_of_band_epg']
        self.external_management_entity_instance = self.args['external_management_entity_instance']

    def read_opt_args(self):
        pass

    def wizard_mode_input_args(self):
        self.management_address['policy_name'] = createNodeManagementAddress.input_key_args()
        self.management_address['optional_args'] = createNodeManagementAddress.input_optional_args()
        self.out_of_band_contract['contract'] = createOutOfBandContract.input_key_args()
        self.out_of_band_contract['optional_args'] = createOutOfBandContract.input_optional_args()
        self.out_of_band_epg = self.out_of_band_contract
        self.external_management_entity_instance['profile_name'] = createExternalManagementEntityInstance.input_key_args()
        self.external_management_entity_instance['optional_args'] = createExternalManagementEntityInstance.input_optional_args()

    def main_function(self):

        # create Node Management Address
        self.look_up_mo('uni/infra/funcprof','')
        createNodeManagementAddress.create_node_management_address(self.mo, self.management_address['policy_name'], optional_args=self.management_address['optional_args'])
        if is_valid_key(self.management_address['optional_args'], 'in_band_management_epg') or is_valid_key(self.management_address['optional_args'], 'out_of_band_management_epg'):
            self.commit_change()
            self.check_if_tenant_exist()
            createNodeManagementAddress.create_ip_address_pool(self.mo, self.management_address['policy_name'], optional_args=self.management_address['optional_args'])
        if is_valid_key(self.management_address['optional_args'], 'fabric_nodes_id'):
            self.commit_change()
            self.look_up_mo('uni/infra', '')
            createNodeManagementAddress.create_infra_nodes(self.mo, self.management_address['policy_name'], self.management_address['optional_args']['fabric_nodes_id'])
        self.commit_change()

        # create out-of-Band Contract
        self.check_if_tenant_exist()
        createOutOfBandContract.create_out_of_band_contract(self.mo, self.out_of_band_contract['contract'], optional_args=self.out_of_band_contract['optional_args'])
        self.commit_change()

        # add Provided Out Of Band Contract
        self.look_up_mo('uni/tn-mgmt/mgmtp-default/oob-default','')
        addMgmtProvidedOutOfBandContract.add_mgmt_provided_out_of_band_contract(self.mo, self.out_of_band_epg['contract'], optional_args=self.out_of_band_epg['optional_args'])
        self.commit_change()

        # create External Management Entity Instance
        self.look_up_mo('uni/tn-mgmt/extmgmt-default', '')
        createExternalManagementEntityInstance.create_external_management_entity_instance(self.mo, self.external_management_entity_instance['profile_name'], optional_args=self.external_management_entity_instance['optional_args'])


if __name__ == '__main__':
    mo = LabConfiguringOutOfBandManagementAccess()
