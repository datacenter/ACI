from cobra.model.fabric import PodPGrp, RsCommPol, RsPodPGrpBGPRRP, RsPodPGrpCoopP, RsPodPGrpIsisDomP, RsSnmpPol, RsTimePol
from createMo import *

DEFAULT_APPLIED_POLICY = 'No'

APPLIED_POLICY_CHOICES = ['yes', 'no']


def input_key_args(msg='\nPlease Specify Pod Policy Group:'):
    print msg
    return input_raw_input("Pod Policy Group Name", required=True)


def input_optional_args(*arg):
    def return_default(msg):
        default = input_yes_no('use default' + msg + ' (default: No)')
        return 'default' if default else ''
    args = {}
    args['date_time_policy'] = return_default('Date Time Policy')
    args['isis_policy'] = return_default('ISIS Policy')
    args['coop_policy'] = return_default('COOP Group Policy')
    args['bgp_policy'] = return_default('BGP Route Reflector Policy')
    args['communication_policy'] = return_default('Communication Policy')
    args['snmp_policy'] = return_default('SNMP Policy')
    return args


def create_pod_policy_group(fabric_funcp, policy_group_name, **args):
    """A POD policy group. This is used for specifying policies to be applied to the leaf nodes, which are part of this POD. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    fabric_podpgrp = PodPGrp(fabric_funcp, policy_group_name)
    fabric_podpgrp_children = RsTimePol(fabric_podpgrp, tnDatetimePolName=args['date_time_policy'])
    fabric_podpgrp_children = RsPodPGrpIsisDomP(fabric_podpgrp, tnIsisDomPolName=args['isis_policy'])
    fabric_podpgrp_children = RsPodPGrpCoopP(fabric_podpgrp, tnCoopPolName=args['coop_policy'])
    fabric_podpgrp_children = RsPodPGrpBGPRRP(fabric_podpgrp, tnBgpInstPolName=args['bgp_policy'])
    fabric_podpgrp_children = RsCommPol(fabric_podpgrp, tnCommPolName=args['communication_policy'])
    fabric_podpgrp_children = RsSnmpPol(fabric_podpgrp, tnSnmpPolName=args['snmp_policy'])


class CreatePodPolicyGroup(CreateMo):

    def __init__(self):
        self.description = 'A POD policy group. This is used for specifying policies to be applied to the leaf nodes, which are part of this POD. '
        self.policy_group = None
        super(CreatePodPolicyGroup, self).__init__()

    def set_cli_mode(self):
        super(CreatePodPolicyGroup, self).set_cli_mode()
        self.parser_cli.add_argument('policy_group', help='The name of the POD policy group. This name can be up to 64 characters. Note that you cannot change this name after the object has been saved.')
        self.parser_cli.add_argument('-d', '--date_time_policy', help='A relation to the date/time policy information.')
        self.parser_cli.add_argument('-I', '--isis_policy', help='A relation to the date/time policy information.')
        self.parser_cli.add_argument('-C', '--coop_policy', help='A relation to the date/time policy information.')
        self.parser_cli.add_argument('-B', '--bgp_policy', help='A relation to the date/time policy information.')
        self.parser_cli.add_argument('-c', '--communication_policy', help='A relation to the date/time policy information.')
        self.parser_cli.add_argument('-S', '--snmp_policy', help='A relation to the date/time policy information.')

    def read_key_args(self):
        self.policy_group = self.args.pop('policy_group')

    def wizard_mode_input_args(self):
        self.args['policy_group'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/fabric/funcprof/podpgrp-', self.policy_group, PodPGrp, description='Policy Group')
        super(CreatePodPolicyGroup, self).delete_mo()

    def main_function(self):
        fabric_funcp = self.look_up_mo('uni/fabric/funcprof/', '')
        create_pod_policy_group(fabric_funcp, self.policy_group, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreatePodPolicyGroup()