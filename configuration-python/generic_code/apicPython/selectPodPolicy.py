from cobra.model.fabric import RsPodPGrp

from createMo import *


def input_key_args(msg='\nPlease Select the Policy Group:'):
    print msg
    return input_raw_input("Fabric Policy Group Name", required=True)


def select_pod_policy(bgp_pods, selected_pod_policy_group, **args):
    """A relation to the pod policy group specifying policies to the leaf nodes in the pod. """
    bgp_rspodpgrp = RsPodPGrp(bgp_pods, tDn='uni/fabric/funcprof/podpgrp-' + selected_pod_policy_group)


class CreateXxxx(CreateMo):

    def __init__(self):
        self.description = 'A relation to the pod policy group specifying policies to the leaf nodes in the pod.'
        self.selected_pod_policy_group = None
        super(CreateXxxx, self).__init__()

    def set_cli_mode(self):
        super(CreateXxxx, self).set_cli_mode()
        self.parser_cli.add_argument('selected_pod_policy_group', help='The distinguished name of the pod policy group.')

    def read_key_args(self):
        self.selected_pod_policy_group = self.args.pop('selected_pod_policy_group')

    def wizard_mode_input_args(self):
        if not self.delete:
            self.args['selected_pod_policy_group'] = input_key_args()
        else:
            self.args['autonomous_system_number'] = None

    def delete_mo(self):
        self.check_if_mo_exist('uni/fabric/podprof-default/pods-default-typ-ALL/rspodPGrp', '', RsPodPGrp, detail_description='No pod policy group has been selected.')
        super(CreateXxxx, self).delete_mo()

    def main_function(self):
        # Query a tenant
        bgp_pods = self.look_up_mo('uni/fabric/podprof-default/pods-default-typ-ALL', '')
        select_pod_policy(bgp_pods, self.selected_pod_policy_group)

if __name__ == '__main__':
    mo = CreateXxxx()