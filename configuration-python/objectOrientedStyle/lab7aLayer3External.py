import setAutonomousSystemNumber
import createBgpRouteReflector
import createPodPolicyGroup
import selectPodPolicy
from createMo import *


class Lab7aLayer3External(CreateMo):
    """
    Integrating With VMware
    """
    def __init__(self):
        self.description = 'Integrating With VMware'
        self.autonomous_system_number = None
        self.reflector_id = []
        self.pod_policy_group = {}
        super(Lab7aLayer3External, self).__init__()

    def set_argparse(self):
        super(Lab7aLayer3External, self).set_argparse()
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
        super(Lab7aLayer3External, self).run_yaml_mode()
        self.autonomous_system_number = self.args['autonomous_system_number']
        self.reflector_id = self.args['reflector_id']
        self.pod_policy_group['name'] = self.args['pod_policy_group']['name']
        self.pod_policy_group['optional_args'] = self.args['pod_policy_group']['optional_args']

    def read_opt_args(self):
        pass

    def wizard_mode_input_args(self):
        self.autonomous_system_number = setAutonomousSystemNumber.input_key_args('')
        reflector_ids = add_mos('Add a Bgp Router Reflector', createBgpRouteReflector.input_key_args)
        for reflector_id in reflector_ids:
            self.reflector_id.append(reflector_id['key_args'])
        pod_policy_group = add_mos('Create a Pod Policy Group', createPodPolicyGroup.input_key_args, createPodPolicyGroup.input_optional_args, do_first=True, once=True)
        self.pod_policy_group['name'] = pod_policy_group['key_args']
        self.pod_policy_group['optional_args'] = pod_policy_group['opt_args']

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


if __name__ == '__main__':
    mo = Lab7aLayer3External()