from labScript import *
import createRoutedOutside
import createNodesAndInterfacesProfile
import createNodes
import createStaticRoute
import createInterfaceProfile
import createRoutedInterfaceProfile
import createExternalNetwork
import createL3EpgProviderOrConsumerContract


class LabConfiguringLayer3ManagementConnectivity(LabScript):
    """
    Integrating With VMware
    """
    def __init__(self):
        self.description = 'Configuring Layer 3 Management Connectivity'
        self.tenant_required = True
        self.tenant = 'mgmt'
        self.routed_outside = {}
        self.node_profile = {}
        self.leaf_id = None
        self.router_id = None
        self.static_route = {}
        self.interface_profile = {}
        self.external_network_epg = {}
        self.consumer_contract = {}
        super(LabConfiguringLayer3ManagementConnectivity, self).__init__()

    def run_yaml_mode(self):
        super(LabConfiguringLayer3ManagementConnectivity, self).run_yaml_mode()
        self.routed_outside = self.args['routed_outside']
        self.node_profile = self.args['node_profile']
        self.leaf_id = self.args['leaf_id']
        self.router_id = self.args['router_id']
        self.static_route = self.args['static_route']
        self.interface_profile = self.args['interface_profile']
        self.external_network_epg = self.args['external_network_epg']
        self.consumer_contract = self.args['consumer_contract']

    def wizard_mode_input_args(self):
        self.routed_outside['name'] = createRoutedOutside.input_key_args()
        self.routed_outside['optional_args'] = createRoutedOutside.input_optional_args()
        self.node_profile['name'] = createNodesAndInterfacesProfile.input_key_args()
        self.node_profile['optional_args'] = createNodesAndInterfacesProfile.input_optional_args()
        self.leaf_id, self.router_id = createNodes.input_key_args()
        self.static_route['prefix'] = createStaticRoute.input_key_args()
        self.static_route['optional_args'] = createStaticRoute.input_optional_args()
        self.interface_profile['name'] = createInterfaceProfile.input_key_args()
        self.interface_profile['leaf_id'], self.interface_profile['eth_num'], self.interface_profile['ip_address'] = createRoutedInterfaceProfile.input_key_args('')
        self.interface_profile['optional_args'] = createRoutedInterfaceProfile.input_optional_args()
        self.external_network_epg['name'] = createExternalNetwork.input_key_args('')
        self.external_network_epg['optional_args'] = createExternalNetwork.input_optional_args()
        self.consumer_contract['name'] = createL3EpgProviderOrConsumerContract.input_key_args(msg='', type_known=True)[0]
        self.consumer_contract['optional_args'] = createL3EpgProviderOrConsumerContract.input_optional_args('consumed')

    def main_function(self):

        # create Bpg Route Outside Network
        self.check_if_tenant_exist()
        l3ext_out = createRoutedOutside.create_routed_outside(self.mo, self.routed_outside['name'], optional_args=self.routed_outside['optional_args'])
        # self.commit_change()

        # create Node-And-Interface Profile
        l3ext_lnodep = createNodesAndInterfacesProfile.create_node_profile(l3ext_out, self.node_profile['name'], optional_args=return_valid_optional_args(self.node_profile))
        # self.commit_change(l3ext_out)

        # create Nodes And Interfaces
        l3ext_rsnodel3outatt = createNodes.create_node(l3ext_lnodep, str(self.leaf_id), str(self.router_id))
        l3ext_lifp = createInterfaceProfile.create_interface_profile(l3ext_lnodep, self.interface_profile['name'])
        # self.commit_change(l3ext_lnodep)

        # create static route
        createStaticRoute.create_static_route(l3ext_rsnodel3outatt, self.static_route['prefix'], optional_args=self.static_route['optional_args'])
        # self.commit_change(l3ext_rsnodel3outatt)

        # create Routed Interface Profile
        createRoutedInterfaceProfile.create_routed_interface_profile(l3ext_lifp, str(self.interface_profile['leaf_id']), str(self.interface_profile['eth_num']), self.interface_profile['ip_address'], optional_args=self.interface_profile['optional_args'])
        # self.commit_change(l3ext_lifp)

        # create External Network
        l3ext_instp = createExternalNetwork.create_external_network(l3ext_out, self.external_network_epg['name'], optional_args=return_valid_optional_args(self.external_network_epg))
        # self.commit_change(l3ext_out)

        # configure provider/consumer for L3 outside network.
        createL3EpgProviderOrConsumerContract.create_L3_epg_provider_or_consumer_contract(l3ext_instp, 'consumed', self.consumer_contract['name'], optional_args=return_valid_optional_args(self.consumer_contract))
        # self.commit_change()


if __name__ == '__main__':
    mo = LabConfiguringLayer3ManagementConnectivity()