from cobra.model.fv import BD, Ctx

from labScript import *
import setAutonomousSystemNumber
import createBgpRouteReflector
import createPodPolicyGroup
import selectPodPolicy
import createRoutedOutside
import createNodesAndInterfacesProfile
import createNodes
import createInterfaceProfile
import createRoutedInterfaceProfile
import createExternalNetwork
import createL3EpgProviderOrConsumerContract
import setDefaultSettingForPrivateNetwork
import associateL3OutsideNetworkToBD


class Lab7aLayer3External(LabScript):
    """
    Integrating With VMware
    """
    def __init__(self):
        self.description = 'Integrating With VMware'
        self.tenant_required = True
        self.autonomous_system_number = None
        self.reflector_id = []
        self.pod_policy_group = {}
        self.routed_outside = {}
        self.node_profile = {}
        self.leaf_id = None
        self.router_id = None
        self.interface_profile = {}
        self.external_network_epg = {}
        self.provider_contract = {}
        self.consumer_contract = {}
        self.private_network = {}
        self.bridge_domain = None
        super(Lab7aLayer3External, self).__init__()

    def run_yaml_mode(self):
        super(Lab7aLayer3External, self).run_yaml_mode()
        self.autonomous_system_number = self.args['autonomous_system_number']
        self.reflector_id = self.args['reflector_id']
        self.pod_policy_group['name'] = self.args['pod_policy_group']['name']
        self.pod_policy_group['optional_args'] = self.args['pod_policy_group']['optional_args']
        self.routed_outside = self.args['routed_outside']
        self.node_profile = self.args['node_profile']
        self.leaf_id = self.args['leaf_id']
        self.router_id = self.args['router_id']
        self.interface_profile = self.args['interface_profile']
        self.external_network_epg = self.args['external_network_epg']
        self.provider_contract = self.args['provider_contract']
        self.consumer_contract = self.args['consumer_contract']
        self.private_network = self.args['private_network']
        self.bridge_domain = self.args['bridge_domain']

    def wizard_mode_input_args(self):
        self.autonomous_system_number = setAutonomousSystemNumber.input_key_args('')
        reflector_ids = add_mos('Add a Bgp Router Reflector', createBgpRouteReflector.input_key_args)
        for reflector_id in reflector_ids:
            self.reflector_id.append(reflector_id['key_args'])
        pod_policy_group = add_mos('Create a Pod Policy Group', createPodPolicyGroup.input_key_args, createPodPolicyGroup.input_optional_args, do_first=True, once=True)
        self.pod_policy_group['name'] = pod_policy_group['key_args']
        self.pod_policy_group['optional_args'] = pod_policy_group['opt_args']
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
        self.provider_contract['name'] = createL3EpgProviderOrConsumerContract.input_key_args(msg='', type_known=True)[0]
        self.provider_contract['optional_args'] = createL3EpgProviderOrConsumerContract.input_optional_args('provided')
        self.consumer_contract['name'] = createL3EpgProviderOrConsumerContract.input_key_args(msg='', type_known=True)[0]
        self.consumer_contract['optional_args'] = createL3EpgProviderOrConsumerContract.input_optional_args('consumed')
        self.private_network['name'] = setDefaultSettingForPrivateNetwork.input_key_args('')
        self.private_network['optional_args'] = setDefaultSettingForPrivateNetwork.input_optional_args()
        self.bridge_domain = associateL3OutsideNetworkToBD.input_key_args('')

    def main_function(self):
        # set Autonomous System Number
        bgp_instpol = self.look_up_mo('uni/fabric/bgpInstP-default', '')
        setAutonomousSystemNumber.set_autonomous_system_number(bgp_instpol, self.autonomous_system_number)
        self.commit_change()

        # create Bpg Route Reflector
        bgp_rrp = self.look_up_mo('uni/fabric/bgpInstP-default/rr', '')
        for reflector_id in self.reflector_id:
            createBgpRouteReflector.create_bgp_route_reflector(bgp_rrp, reflector_id)
        self.commit_change()

        # create Pod Policy group
        fabric_funcp = self.look_up_mo('uni/fabric/funcprof/', '')
        createPodPolicyGroup.create_pod_policy_group(fabric_funcp, self.pod_policy_group['name'], optional_args=self.pod_policy_group['optional_args'])
        self.commit_change()

        # select Pod Policy
        bgp_pods = self.look_up_mo('uni/fabric/podprof-default/pods-default-typ-ALL', '')
        selectPodPolicy.select_pod_policy(bgp_pods, self.pod_policy_group['name'])

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
        l3ext_instp = createExternalNetwork.create_external_network(l3ext_out, self.external_network_epg['name'], optional_args=self.external_network_epg['optional_args'])
        self.commit_change(l3ext_out)

        # configure provider/consumer for L3 outside network.
        createL3EpgProviderOrConsumerContract.create_L3_epg_provider_or_consumer_contract(l3ext_instp, 'provided', self.provider_contract['name'], optional_args=self.provider_contract['optional_args'])
        createL3EpgProviderOrConsumerContract.create_L3_epg_provider_or_consumer_contract(l3ext_instp, 'consumed', self.consumer_contract['name'], optional_args=self.consumer_contract['optional_args'])
        self.commit_change()

        # Set default settings for private network.
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/ctx-', self.private_network['name'], Ctx, description='Private Network')
        setDefaultSettingForPrivateNetwork.set_default_setting_for_private_network(self.mo, optional_args=self.private_network['optional_args'])
        self.commit_change()

        # Associate the L3 Outside Network to a Birdge Domain.
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/BD-', self.bridge_domain, BD, description='Bridge Domain')
        associateL3OutsideNetworkToBD.associate_l3_outside_network_to_bd(self.mo, self.routed_outside['name'])

if __name__ == '__main__':
    mo = Lab7aLayer3External()