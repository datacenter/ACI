from cobra.model.infra import AccBndlGrp, RsAttEntP, RsHIfPol, RsCdpIfPol, RsLldpIfPol, RsStpIfPol, RsLacpPol, RsMonIfInfraPol, ConnNodeS, HConnPortS, ConnNodeBlk, RsConnPortS, ConnPortBlk, RsSpanVSrcGrp, RsSpanVDestGrp, AccBndlSubgrp, RsLacpIfPol


from createMo import *


DEFAULT_POLICY = None

CHOICES = []


def input_key_args(msg='\nPlease Specify the PC Interface Policy Group:'):
    print msg
    return input_raw_input("PC Interface Policy Group Name", required=True)


def input_interface():
    return input_raw_input('Interface (eg: 1/14, 1/13-15, 101/13-15)', required=True)


def input_connectivity_filter(msg='Please specify the Connectivity Filters:'):
    print msg
    args = {}
    args['switch_id'] = input_raw_input('Switch IDs', required=True)
    args['interfaces'] = read_add_mos_args(add_mos('Add an Interface', input_interface))
    return args


def input_vsource_group():
    return input_raw_input('VSource Group', required=True)


def input_vdestination_group():
    return input_raw_input('VDestination Group', required=True)


def input_override_policy_group():
    return {'name':input_raw_input('Override Policy Group', required=True),
            'lacp_member': input_raw_input('LACP Member Policy')}


def input_optional_args():
    args = {}
    args['link_level'] = input_raw_input("Link Level Policy", default=DEFAULT_POLICY)
    args['cdp'] = input_raw_input("CDP Policy", default=DEFAULT_POLICY)
    args['lldp'] = input_raw_input("LLDP Policy", default=DEFAULT_POLICY)
    args['stp_interface'] = input_raw_input("STP Interface Policy", default=DEFAULT_POLICY)
    args['lacp'] = input_raw_input('LACP Policy', default=DEFAULT_POLICY)
    args['monitoring'] = input_raw_input("Monitoring Policy", default=DEFAULT_POLICY)
    args['entity_profile'] = input_raw_input("Attached Entity Profile", default=DEFAULT_POLICY)
    if args['entity_profile'] != '' and args['entity_profile'] is not None:
        args['connectivity_filters'] = read_add_mos_args(add_mos('Add a Connectivity Filter', input_connectivity_filter))
    args['vsource_groups'] = read_add_mos_args(add_mos('Add a VSsource Group', input_vsource_group))
    args['vdestination_groups'] = read_add_mos_args(add_mos('Add a VDestination Group', input_vdestination_group))
    args['override_policy_groups'] = read_add_mos_args(add_mos('Add an Override Policy Group', input_override_policy_group))

    return args

def create_pc_interface_policy_group(parent_mo, group_name, **args):
    """Create a PC Interface Policy Group"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    infra_accbndlgrp = AccBndlGrp(parent_mo, group_name)

    if is_valid_key(args, 'link_level'):
        infra_rshifpol = RsHIfPol(infra_accbndlgrp, tnFabricHIfPolName=args['link_level'])
    if is_valid_key(args, 'cdp'):
        infra_rscdpifpol = RsCdpIfPol(infra_accbndlgrp, tnCdpIfPolName=args['cdp'])
    if is_valid_key(args, 'lldp'):
        infra_rslldpifpol = RsLldpIfPol(infra_accbndlgrp, tnLldpIfPolName=args['lldp'])
    if is_valid_key(args, 'stp_interface'):
        infra_rsstpifpol = RsStpIfPol(infra_accbndlgrp, tnStpIfPolName=args['stp_interface'])
    if is_valid_key(args, 'lacp'):
        infra_rsmonifinfrapol = RsLacpPol(infra_accbndlgrp, tnLacpLagPolName=args['lacp'])
    if is_valid_key(args, 'monitoring'):
        infra_rsmonifinfrapol = RsMonIfInfraPol(infra_accbndlgrp, tnMonInfraPolName=args['monitoring'])
    if is_valid_key(args, 'entity_profile'):
        infra_rsattentp = RsAttEntP(infra_accbndlgrp, tDn='uni/infra/attentp-'+args['entity_profile'])
        def add_connectivity_filter(index, filter):
            infra_connnodes = ConnNodeS(infra_rsattentp, 'selector'+str(filter['switch_id']))
            infra_hconnports = HConnPortS(infra_rsattentp, 'selector'+str(filter['switch_id'])+'LeafPorts', 'range')
            infra_connnodeblk = ConnNodeBlk(infra_connnodes, 'block'+str(index), from_=str(filter['switch_id']), to_=str(filter['switch_id']))
            infra_rsconnports = RsConnPortS(infra_connnodes, 'uni/infra/funcprof/accbundle-'+group_name+'/rsattEntP/hports-selector'+str(filter['switch_id'])+'LeafPorts-typ-range')
            id = 0
            for interface in filter['interfaces']:
                id += 1
                card, fromPort, toPort = input_ports(interface)
                infra_connportblk = ConnPortBlk(infra_hconnports, 'block'+str(id), fromPort=fromPort, toPort=toPort)

        if is_valid_key(args, 'connectivity_filters'):
            idx = 0
            for connectivity_filter in args['connectivity_filters']:
                idx += 1
                add_connectivity_filter(idx, connectivity_filter)

    if is_valid_key(args, 'vsource_groups'):
        for vsource_group in args['vsource_groups']:
            infra_rsspanvsrcggrp = RsSpanVSrcGrp(infra_accbndlgrp, vsource_group)

    if is_valid_key(args, 'vdestination_groups'):
        for vdestination_group in args['vdestination_groups']:
            infra_rsspanvdestgrp = RsSpanVDestGrp(infra_accbndlgrp, vdestination_group)

    if is_valid_key(args, 'override_policy_groups'):
        for override_policy_group in args['override_policy_groups']:
            infra_accbndlsubgrp = AccBndlSubgrp(infra_accbndlgrp, override_policy_group['name'])
            if is_valid_key(override_policy_group, 'lacp_member'):
                infra_rslacpifpol = RsLacpIfPol(infra_accbndlsubgrp, tnLacpIfPolName=override_policy_group['lacp_member'])

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
        self.parser_cli.add_argument('-f', '--connectivity_filter',nargs='+', action='append', help='Connectivity Filter')
        self.parser_cli.add_argument('-S', '--vsource_groups',nargs='+', help='VSource Groups. A relation to all endpoints with traffic that will be spanned.')
        self.parser_cli.add_argument('-D', '--vdestination_groups',nargs='+', help='VDestination Groups. A relation to all end points (or IP in the case of ERSPAN) to which the SPAN packets will be spanned.')
        self.parser_cli.add_argument('-O', '--override_policy_groups',nargs='+', action='append', help='The access bundle subgroup, which enables you to specify (override) a different LACP member policy name for some of the interfaces that are part of an access bundle group.')

    def read_key_args(self):
        self.group = self.args.pop('group')

    def wizard_mode_input_args(self):
        self.args['group'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def run_cli_mode(self):
        super(CreatePcInterfacePolicyGroup, self).run_cli_mode()
        if is_valid_key(self.args, 'connectivity_filter'):
            connectivity_filters = []
            for connectivity_filter in self.args['connectivity_filter']:
                connectivity_filters.append({'switch_id': connectivity_filter.pop(0),
                                             'interfaces': connectivity_filter})
            self.args['connectivity_filters'] = connectivity_filters
        if is_valid_key(self.args, 'override_policy_groups'):
            override_policy_groups = []
            for override_policy_group in self.args['override_policy_groups']:
                if len(override_policy_group) < 2:
                    override_policy_group.append('')
                override_policy_groups.append({'name': override_policy_group[0],
                                               'lacp_member': override_policy_group[1]})
            self.args['override_policy_groups'] = override_policy_groups

    def delete_mo(self):
        self.check_if_mo_exist('uni/infra/funcprof/accbundle-', self.group, AccBndlGrp, description='PC Interface Policy Group')
        super(CreatePcInterfacePolicyGroup, self).delete_mo()

    def main_function(self):
        # Query a parent
        self.look_up_mo('uni/infra/funcprof/', '')
        create_pc_interface_policy_group(self.mo, self.group, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreatePcInterfacePolicyGroup()


