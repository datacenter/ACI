from cobra.model.infra import AccBndlGrp, RsAttEntP, RsHIfPol, RsCdpIfPol, RsLldpIfPol, RsStpIfPol, RsLacpIfPol, RsMonIfInfraPol

from createMo import *


DEFAULT_POLICY = None

CHOICES = []


def input_key_args(msg='\nPlease Specify the PC Interface Policy Group:'):
    print msg
    return input_raw_input("PC Interface Policy Group Name", required=True)


def input_optional_args():
    args = {}
    args['link_level'] = input_raw_input("Link Level Policy", default=DEFAULT_POLICY)
    args['cdp'] = input_raw_input("CDP Policy", default=DEFAULT_POLICY)
    args['lldp'] = input_raw_input("LLDP Policy", default=DEFAULT_POLICY)
    args['stp_interface'] = input_raw_input("STP Interface Policy", default=DEFAULT_POLICY)
    args['lacp'] = input_raw_input('LACP Policy', default=DEFAULT_POLICY)
    args['monitoring'] = input_raw_input("Monitoring Policy", default=DEFAULT_POLICY)
    args['entity_profile'] = input_raw_input("Attached Entity Profile", default=DEFAULT_POLICY)

    return args


def create_pc_interface_policy_group(parent_mo, mo, **args):
    """Create a PC Interface Policy Group"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    infra_accbndlgrp = AccBndlGrp(parent_mo, mo)

    if is_valid_key(args, 'link_level'):
        infra_rshifpol = RsHIfPol(infra_accbndlgrp, tnFabricHIfPolName=args['link_level'])
    if is_valid_key(args, 'cdp'):
        infra_rscdpifpol = RsCdpIfPol(infra_accbndlgrp, tnCdpIfPolName=args['cdp'])
    if is_valid_key(args, 'lldp'):
        infra_rslldpifpol = RsLldpIfPol(infra_accbndlgrp, tnLldpIfPolName=args['lldp'])
    if is_valid_key(args, 'stp_interface'):
        infra_rsstpifpol = RsStpIfPol(infra_accbndlgrp, tnStpIfPolName=args['stp_interface'])
    if is_valid_key(args, 'lacp'):
        infra_rsmonifinfrapol = RsLacpIfPol(infra_accbndlgrp, tnLacpLagPolName=args['lacp'])
    if is_valid_key(args, 'monitoring'):
        infra_rsmonifinfrapol = RsMonIfInfraPol(infra_accbndlgrp, tnMonInfraPolName=args['monitoring'])
    if is_valid_key(args, 'entity_profile'):
        infra = RsAttEntP(infra_accbndlgrp, tDn='uni/infra/attentp-'+args['entity_profile'])

    return infra_accbndlgrp


class CreatePcInterfacePolicyGroup(CreateMo):

    def __init__(self):
        self.description = 'Create a PC Interface Policy Group. The bundle interface group, which enables you to specify the interface policy you want to use. '
        self.group = None
        super(CreatePcInterfacePolicyGroup, self).__init__()

    def set_cli_mode(self):
        super(CreatePcInterfacePolicyGroup, self).set_cli_mode()
        self.parser_cli.add_argument('group', help='Group Name.')
        self.parser_cli.add_argument('-L', '--link_level', default= DEFAULT_POLICY, help='The physical interface policy name. A relation to the host interface policy.')
        self.parser_cli.add_argument('-c', '--cdp', default= DEFAULT_POLICY, help='The CDP policy name. A relation to the CDP Interface Policy.')
        self.parser_cli.add_argument('-l', '--lldp', default= DEFAULT_POLICY, help='The LLDP policy name. A relation to the LLDP policy parameters for the interface.')
        self.parser_cli.add_argument('-s', '--stp_interface', default= DEFAULT_POLICY, help='The STP policy name. A relation to the spanning-tree protocol (STP) policy.')
        self.parser_cli.add_argument('-a', '--lacp', default= DEFAULT_POLICY, help='The LACP policy name. A relation to the port level LACP member policy configured parameters.')
        self.parser_cli.add_argument('-m', '--monitoring', default= DEFAULT_POLICY, help='The monitoring policy name. A relation to the monitoring policy model.')
        self.parser_cli.add_argument('-e', '--entity_profile', default= DEFAULT_POLICY, help='The Entity Profile name. A relation to the attached entity profile.')
        self.parser_cli.add_argument('-I', '--switch_id', default= DEFAULT_POLICY, help='Switch ID.')
        self.parser_cli.add_argument('-i', '--interfaces', default= DEFAULT_POLICY, help='Interfaces.')

    def read_key_args(self):
        self.group = self.args.pop('group')

    def wizard_mode_input_args(self):
        self.args['group'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/infra/funcprof/accbundle-', self.group, AccBndlGrp, description='PC Interface Policy Group')
        super(CreatePcInterfacePolicyGroup, self).delete_mo()

    def main_function(self):
        # Query a parent
        self.look_up_mo('uni/infra/funcprof/', '')
        create_pc_interface_policy_group(self.mo, self.group, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreatePcInterfacePolicyGroup()


