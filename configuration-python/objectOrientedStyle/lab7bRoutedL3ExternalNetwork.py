import createRoutedOutside 
import createNodesAndInterfacesProfile
import createNodes 
import createInterfaceProfile 
import createRoutedInterfaceProfile 
import createExternalNetwork 

from createMo import *


class Lab7bRoutedL3ExternalNetwork(CreateMo):
    """
    Configure routed L3 external network.
    """
    def __init__(self):
        self.description = 'Configure routed L3 external network.'
        self.tenant_required = True
        self.routed_outside = {}
        self.node_profile = {}
        self.leaf_id = None
        self.router_id = None
        self.interface_profile = {}
        self.external_network_epg = {}
        super(Lab7bRoutedL3ExternalNetwork, self).__init__()

    def set_argparse(self):
        super(Lab7bRoutedL3ExternalNetwork, self).set_argparse()
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
        super(Lab7bRoutedL3ExternalNetwork, self).run_yaml_mode()
        self.routed_outside = self.args['routed_outside']
        self.node_profile = self.args['node_profile']
        self.leaf_id = self.args['leaf_id']
        self.router_id = self.args['router_id']
        self.interface_profile = self.args['interface_profile']
        self.external_network_epg = self.args['external_network_epg']

    def read_opt_args(self):
        pass

    def wizard_mode_input_args(self):
        self.routed_outside['name'] = createRoutedOutside.input_key_args('')
        self.routed_outside['optional_args'] = createRoutedOutside.input_optional_args()
        self.node_profile['name'] = createNodesAndInterfacesProfile.input_key_args('')
        self.node_profile['optional_args'] = createNodesAndInterfacesProfile.input_optional_args()
        self.leaf_id, self.router_id = createNodes.input_key_args('')
        self.interface_profile['name'] = createInterfaceProfile.input_key_args('')
        self.interface_profile['leaf_id'], self.interface_profile['eth_num'], self.interface_profile['ip_address'] = createRoutedInterfaceProfile.input_key_args('')
        self.interface_profile['optional_args'] = createRoutedInterfaceProfile.input_optional_args()
        self.external_network_epg['name'] = createExternalNetwork.input_key_args('')
        self.external_network_epg['optional_args'] = createExternalNetwork.input_optional_args()

    def main_function(self):

        # create Bpg Route Outside Network
        self.check_if_tenant_exist()
        l3ext_out = createRoutedOutside.create_routed_outside(self.mo, self.routed_outside['name'], optional_args=self.routed_outside['optional_args'])
        self.commit_change()

        # create Node-And-Interface Profile
        l3ext_lnodep = createNodesAndInterfacesProfile.create_node_profile(l3ext_out, self.node_profile['name'], optional_args=self.node_profile['optional_args'])
        self.commit_change(l3ext_out)

        # create Nodes And Interfaces
        createNodes.create_node(l3ext_lnodep, str(self.leaf_id), str(self.router_id))
        l3ext_lifp = createInterfaceProfile.create_interface_profile(l3ext_lnodep, self.interface_profile['name'])
        self.commit_change(l3ext_lnodep)

        # create Routed Interface Profile
        createRoutedInterfaceProfile.create_routed_interface_profile(l3ext_lifp, str(self.interface_profile['leaf_id']), str(self.interface_profile['eth_num']), self.interface_profile['ip_address'], optional_args=self.interface_profile['optional_args'])
        self.commit_change(l3ext_lifp)

        # create External Network
        createExternalNetwork.create_external_network(l3ext_out, self.external_network_epg['name'], optional_args=self.external_network_epg['optional_args'])
        self.commit_change(l3ext_out)


if __name__ == '__main__':
    mo = Lab7bRoutedL3ExternalNetwork()