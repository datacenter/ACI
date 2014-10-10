from labScript import *

from apicPython import createRoutedOutside
from apicPython import createNodesAndInterfacesProfile
from apicPython import createNodes
from apicPython import createInterfaceProfile
from apicPython import createRoutedInterfaceProfile
from apicPython import createExternalNetwork


class LabConfiguringMpBgpRouteReflector(LabScript):

    def __init__(self):
        self.description = 'Configuring a DNS Server Policy.'
        self.tenant_required = True
        self.routed_outside = {}
        self.node_profile = None
        self.select_nodes = []
        self.interface_profile = None
        self.select_routed_interfaces = []
        self.external_network = None
        super(LabConfiguringMpBgpRouteReflector, self).__init__()

    def run_yaml_mode(self):
        super(LabConfiguringMpBgpRouteReflector, self).run_yaml_mode()
        self.routed_outside = self.args['routed_outside']
        self.node_profile = self.args['node_profile']
        self.select_nodes = self.args['select_nodes']
        self.interface_profile = self.args['interface_profile']
        self.select_routed_interfaces = self.args['select_routed_interfaces']
        self.external_network = self.args['external_network']

    def wizard_mode_input_args(self):
        self.routed_outside['name'] = createRoutedOutside.input_key_args()
        self.routed_outside['optional_args'] = createRoutedOutside.input_optional_args()
        self.node_profile = createNodesAndInterfacesProfile.input_key_args()
        self.select_nodes = read_add_mos_args(add_mos('Add a node', createNodes.input_key_args))
        select_nodes = []
        for node in self.select_nodes:
            select_nodes.append({'leaf_id': node[0],
                                 'router_id': node[1]})
        self.select_nodes = select_nodes
        self.interface_profile = createInterfaceProfile.input_key_args()
        self.select_routed_interfaces = read_add_mos_args(add_mos('Add a Routed Interface', createRoutedInterfaceProfile.input_key_args))
        select_routed_interfaces = []
        for interface in self.select_routed_interfaces:
            select_routed_interfaces.append({'leaf_id': interface[0],
                                             'eth_num': interface[1],
                                             'ip_address': interface[2]})
        self.select_routed_interfaces = select_routed_interfaces
        self.external_network = createExternalNetwork.input_key_args()

    def main_function(self):

        # create Bpg Route Outside Network
        self.check_if_tenant_exist()
        l3ext_out = createRoutedOutside.create_routed_outside(self.mo, self.routed_outside['name'], optional_args=return_valid_optional_args(self.routed_outside))
        self.commit_change()

        # create Node-And-Interface Profile
        l3ext_lnodep = createNodesAndInterfacesProfile.create_node_profile(l3ext_out, self.node_profile, optional_args=return_valid_optional_args(self.node_profile))
        self.commit_change(l3ext_out)

        # create Nodes And Interfaces
        for node in self.select_nodes:
            createNodes.create_node(l3ext_lnodep, str(node['leaf_id']), str(node['router_id']))
        l3ext_lifp = createInterfaceProfile.create_interface_profile(l3ext_lnodep, self.interface_profile)
        self.commit_change(l3ext_lnodep)

        # create Routed Interface Profile
        for interface in self.select_routed_interfaces:
            createRoutedInterfaceProfile.create_routed_interface_profile(l3ext_lifp, str(interface['leaf_id']), str(interface['eth_num']), interface['ip_address'], optional_args=return_valid_optional_args(interface))
        self.commit_change(l3ext_lifp)

        # create External Network
        l3ext_instp = createExternalNetwork.create_external_network(l3ext_out, self.external_network, optional_args=return_valid_optional_args(self.external_network))
        self.commit_change(l3ext_out)

if __name__ == '__main__':
    mo = LabConfiguringMpBgpRouteReflector()