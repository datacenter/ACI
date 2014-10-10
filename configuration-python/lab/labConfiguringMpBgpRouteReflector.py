from labScript import *

from apicPython import setAutonomousSystemNumber
from apicPython import createBgpRouteReflector
from apicPython import createPodPolicyGroup
from apicPython import selectPodPolicy


class LabConfiguringMpBgpRouteReflector(LabScript):

    def __init__(self):
        self.description = 'Configuring a DNS Server Policy.'
        self.autonomous_system_number = None
        self.reflector_ids = []
        self.policy_group = None
        super(LabConfiguringMpBgpRouteReflector, self).__init__()

    def run_yaml_mode(self):
        super(LabConfiguringMpBgpRouteReflector, self).run_yaml_mode()
        self.autonomous_system_number = self.args['autonomous_system_number']
        self.reflector_ids = self.args['reflector_ids']
        self.policy_group = self.args['policy_group']
        self.optional_args = self.args['optional_args']

    def wizard_mode_input_args(self):
        self.autonomous_system_number = setAutonomousSystemNumber.input_key_args()
        self.reflector_ids = read_add_mos_args(add_mos('Add a route reflector node', createBgpRouteReflector.input_key_args))
        self.policy_group = createPodPolicyGroup.input_key_args()
        self.optional_args = createPodPolicyGroup.input_optional_args()

    def main_function(self):

        # set autonomous system number
        self.look_up_mo('uni/fabric/bgpInstP-default', '')
        setAutonomousSystemNumber.set_autonomous_system_number(self.mo, self.autonomous_system_number)
        self.commit_change()

        # Create node route reflectors
        self.look_up_mo('uni/fabric/bgpInstP-default/rr', '')
        for reflector_id in self.reflector_ids:
            createBgpRouteReflector.create_bgp_route_reflector(self.mo, reflector_id)
        self.commit_change()

        # create Pod Policy Group
        self.look_up_mo('uni/fabric/funcprof/', '')
        createPodPolicyGroup.create_pod_policy_group(self.mo, self.policy_group, optional_args=self.optional_args)
        self.commit_change()

        # set the Pod Policy Group as default
        self.look_up_mo('uni/fabric/podprof-default/pods-default-typ-ALL', '')
        selectPodPolicy.select_pod_policy(self.mo, self.policy_group)

if __name__ == '__main__':
    mo = LabConfiguringMpBgpRouteReflector()