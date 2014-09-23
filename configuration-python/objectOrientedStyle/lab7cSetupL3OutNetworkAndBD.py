from cobra.model.fv import BD, Ctx
from cobra.model.l3ext import Out, InstP

import createRoutedOutside
import createExternalNetwork
import createL3EpgProviderOrConsumerContract
import setDefaultSettingForPrivateNetwork
import associateL3OutsideNetworkToBD

from createMo import *


class Lab7cSetupL3OutNetworkAndBD(CreateMo):
    """
    Enable user to Enable user to load a config file (yaml format) in order to configure provider/consumer for external network epg, set setting for private network and associate the l3 outside network to a bridge domain.
    """
    def __init__(self):
        self.description = 'Enable user to Enable user to load a config file (yaml format) in order to configure provider/consumer for external network epg, set setting for private network and associate the l3 outside network to a bridge domain.'
        self.tenant_required = True
        self.routed_outside = None
        self.external_network_epg = None
        self.provider_contract = {}
        self.consumer_contract = {}
        self.private_network = {}
        self.bridge_domain = None
        super(Lab7cSetupL3OutNetworkAndBD, self).__init__()

    def set_argparse(self):
        super(Lab7cSetupL3OutNetworkAndBD, self).set_argparse()
        self.parser_cli = self.subparsers.add_parser(
            'cli', help='Not Support.'
        )

    def delete_mo(self):
        print 'Delete method is not supported in this function.'
        sys.exit()

    def set_cli_mode(self):
        pass

    def run_cli_mode(self):
        print 'CLI mode is not supported in this method. Please try Yaml mode or Wizard mode.'
        sys.exit()

    def run_yaml_mode(self):
        super(Lab7cSetupL3OutNetworkAndBD, self).run_yaml_mode()
        self.routed_outside = self.args['routed_outside']
        self.external_network_epg = self.args['external_network_epg']
        self.provider_contract = self.args['provider_contract']
        self.consumer_contract = self.args['consumer_contract']
        self.private_network = self.args['private_network']
        self.bridge_domain = self.args['bridge_domain']

    def read_opt_args(self):
        pass

    def wizard_mode_input_args(self):
        self.routed_outside = createRoutedOutside.input_key_args('')
        self.external_network_epg = createExternalNetwork.input_key_args('')
        self.provider_contract['name'] = createL3EpgProviderOrConsumerContract.input_key_args(msg='', type_known=True)[0]
        self.provider_contract['optional_args'] = createL3EpgProviderOrConsumerContract.input_optional_args('provided')
        self.consumer_contract['name'] = createL3EpgProviderOrConsumerContract.input_key_args(msg='', type_known=True)[0]
        self.consumer_contract['optional_args'] = createL3EpgProviderOrConsumerContract.input_optional_args('consumed')
        self.private_network['name'] = setDefaultSettingForPrivateNetwork.input_key_args('')
        self.private_network['optional_args'] = setDefaultSettingForPrivateNetwork.input_optional_args()
        self.bridge_domain = associateL3OutsideNetworkToBD.input_key_args('')

    def main_function(self):

        self.check_if_tenant_exist()
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-', self.routed_outside, Out, description='The policy')
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/instP-', self.external_network_epg, InstP, description='External Netwrok')
        createL3EpgProviderOrConsumerContract.create_L3_epg_provider_or_consumer_contract(self.mo, 'provided', self.provider_contract['name'], optional_args=self.provider_contract['optional_args'])
        createL3EpgProviderOrConsumerContract.create_L3_epg_provider_or_consumer_contract(self.mo, 'consumed', self.consumer_contract['name'], optional_args=self.consumer_contract['optional_args'])
        self.commit_change()

        self.check_if_mo_exist('uni/tn-' + self.tenant + '/ctx-', self.private_network['name'], Ctx, description='Private Network')
        setDefaultSettingForPrivateNetwork.set_default_setting_for_private_network(self.mo, optional_args=self.private_network['optional_args'])
        self.commit_change()

        self.check_if_mo_exist('uni/tn-' + self.tenant + '/BD-', self.bridge_domain, BD, description='Bridge Domain')
        associateL3OutsideNetworkToBD.associate_l3_outside_network_to_bd(self.mo, self.routed_outside)

if __name__ == '__main__':
    mo = Lab7cSetupL3OutNetworkAndBD()