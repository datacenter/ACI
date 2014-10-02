from cobra.model.infra import AccPortP, HPortS, PortBlk, RsAccBaseGrp, NodeP, LeafS, NodeBlk, RsAccPortP, AccPortGrp, AccBndlGrp

from createMo import *

DEFAULT_INTERFACE_TYPE = 'individual'
DEFAULT_TYPE = 'range'

INTERFACE_TYPE_CHOICES = ['individual', 'pc', 'vpc']


def input_key_args(msg='\nPlease Specify the Interface Profile:', delete_function=False):
    print msg
    args = []
    args.append(input_raw_input("Switch Profile Name", required=True))
    if not delete_function:
        def input_switches():
            return input_raw_input("Switches ID", required=True)

        def input_interfaces_ports():
            return input_raw_input("Interfaces Ports", required=True)
        args.append(read_add_mos_args(add_mos('Add a Switch?', input_switches, do_first=True)))
        args.append(input_options("Interface Type", DEFAULT_INTERFACE_TYPE, INTERFACE_TYPE_CHOICES))
        args.append(read_add_mos_args(add_mos('Add a Port?', input_interfaces_ports, do_first=True)))
        args.append(input_raw_input("Interface Selector Name", required=True))
        args.append(input_raw_input("Interface Policy Group", required=True))
    else:
        args.extend([None, None, None, None, None])
    return args


def configure_interface_pc_and_vpc(infra, switch_profile, switches, interface_type, ports, selector, policy_group):
    """The interface profile, which enables you to specify the interface you want to configure. """
    infra_accportp = AccPortP(infra, switch_profile + '_ifselector')
    infra_hports = HPortS(infra_accportp, selector, DEFAULT_TYPE)
    block = 0
    for port in ports:
        block += 1
        card, fromPort, toPort = input_ports(port)
        infra_portblk = PortBlk(infra_hports, 'block'+str(block), fromCard=card, fromPort=fromPort, toPort=toPort)
    if interface_type == 'individual':
        policy_group_type = 'accportgrp'
    elif interface_type in ['pc', 'PC', 'VPC', 'vpc']:
        policy_group_type = 'accbundle'
    else:
        print 'Invalid interface type. Option of interface type is "individual", "pc" or, "vpc".'
        sys.exit()
    infra_rsaccbasegrp = RsAccBaseGrp(infra_hports, tDn='uni/infra/funcprof/' + policy_group_type + '-' + policy_group)

    infra_nodep = NodeP(infra, switch_profile)
    infra_leafs = LeafS(infra_nodep, switch_profile+'_selector_'+''.join(map(str,switches)), DEFAULT_TYPE)
    single = 0
    for switch in switches:
        single += 1
        infra_nodeblk = NodeBlk(infra_leafs, 'single'+str(single), from_=str(switch), to_=str(switch))

    infra_rsaccportp = RsAccPortP(infra_nodep, 'uni/infra/accportprof-'+switch_profile+'_ifselector')


class ConfigureInterfacePcAndVpc(CreateMo):

    def __init__(self):
        self.description = 'The interface profile, which enables you to specify the interface you want to configure. '
        self.switch_profile = None
        self.interface_selector = None
        self.interface_policy_group = None
        self.interface_type = None
        self.switches = None
        self.interface_ports = None
        super(ConfigureInterfacePcAndVpc, self).__init__()

    def set_cli_mode(self):
        super(ConfigureInterfacePcAndVpc, self).set_cli_mode()
        self.parser_cli.add_argument('switch_profile', help='The interface profile name.')
        self.parser_cli.add_argument('interface_type', choices=INTERFACE_TYPE_CHOICES, help='A relation to the access policy group providing port configuration.')
        self.parser_cli.add_argument('interface_selector', help='The Host Port Selector is used for grouping ports between the node and the host (such as hypervisor).')
        self.parser_cli.add_argument('interface_policy_group', help='A relation to the access policy group providing port configuration.')
        self.parser_cli.add_argument('-s', '--switches', nargs="*", help='Switches ID (could be more than 1)', required=True)
        self.parser_cli.add_argument('-p', '--interface_ports', nargs="*", help='Interfaces Ports (eg: 1/12, 1/15-18, 101/32)', required=True)

    def read_key_args(self):
        self.switch_profile = self.args.pop('switch_profile')
        self.interface_selector = self.args.pop('interface_selector')
        self.interface_policy_group = self.args.pop('interface_policy_group')
        self.interface_type = self.args.pop('interface_type')
        self.switches = self.args.pop('switches')
        self.interface_ports = self.args.pop('interface_ports')

    def wizard_mode_input_args(self):
        self.args['switch_profile'], self.args['switches'], self.args['interface_type'], self.args['interface_ports'], self.args['interface_selector'], self.args['interface_policy_group'] = input_key_args(delete_function=self.delete)

    def delete_mo(self):
        self.check_if_mo_exist('uni/infra/accportprof-' + self.switch_profile + '_ifselector', module=AccPortP, description='Interface Profile')
        self.mo.delete()
        self.commit_change()
        self.check_if_mo_exist('uni/infra/nprof-', self.switch_profile, module=NodeP, description='Switch Profile')
        self.mo.delete()

    def main_function(self):
        self.look_up_mo('uni/infra', '')
        if self.interface_type == 'individual':
            if not self.check_if_mo_exist('uni/infra/funcprof/accportgrp-', self.interface_policy_group, AccPortGrp, 'Interface Policy Group', return_false=True, set_mo=False):
                sys.exit()
        elif self.interface_type in ['pc', 'PC', 'VPC', 'vpc']:
            if not self.check_if_mo_exist('uni/infra/funcprof/accbundle-', self.interface_policy_group, AccBndlGrp, self.interface_type+' Policy Group', return_false=True, set_mo=False):
                sys.exit()
        configure_interface_pc_and_vpc(self.mo, self.switch_profile, self.switches, self.interface_type, self.interface_ports, self.interface_selector, self.interface_policy_group)

if __name__ == '__main__':
    mo = ConfigureInterfacePcAndVpc()



