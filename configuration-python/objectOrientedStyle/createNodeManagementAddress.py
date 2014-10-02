from cobra.model.mgmt import Grp, InBZone, OoBZone, RsAddrInst, RsInbEpg, RsOobEpg, NodeGrp, RsGrp
from cobra.model.infra import NodeBlk
from cobra.model.fvns import AddrInst, UcastAddrBlk

from createMo import *

DEFAULT_CONSTANT = 'unspecified'
DEFAULT_IN_BAND_ADDRESS = 'no'
DEFAULT_Out_of_BAND_ADDRESS = 'no'


def input_node():
    return input_raw_input('Node ID', required=True)


def input_key_args(msg='\nPlease Specify policy name, select nodes to be included in the group, and set their IPs:'):
    print msg
    return input_raw_input("Policy Name", required=True)


def input_optional_args():
    args = {}
    args['fabric_nodes_id'] = read_add_mos_args(add_mos('Add a Node', input_node, do_first=True))

    args['in_band_address'] = input_yes_no('Config In-Band Address', default=DEFAULT_IN_BAND_ADDRESS)
    if args['in_band_address']:
        args['in_band_management_epg'] = input_raw_input('In-Band Maanagement EPG', required=True)
        args['in_band_gateway'] = input_raw_input('In-Band Gateway', required=True)
        args['in_band_ip_address_from'] = input_raw_input('In-Band IP Address From', required=True)
        args['in_band_ip_address_to'] = input_raw_input('In-Band IP Address To', required=True)

    args['out_of_band_address'] = input_yes_no('Config Out-of-Band Address', default=DEFAULT_Out_of_BAND_ADDRESS)
    if args['out_of_band_address']:
        args['out_of_band_management_epg'] = input_raw_input('Out-of-Band Maanagement EPG', required=True)
        args['out_of_band_gateway'] = input_raw_input('Out-of-Band Gateway', required=True)
        args['out_of_band_ip_address_from'] = input_raw_input('Out-of-Band IP Address From', required=True)
        args['out_of_band_ip_address_to'] = input_raw_input('Out-of-Band IP Address To', required=True)

    return args


def create_node_management_address(parent_mo, policy_name, **args):
    """Create Node Management Address"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    mgmt_grp = Grp(parent_mo, policy_name)
    if is_valid_key(args, 'in_band_management_epg'):
        mgmt_inbzone = InBZone(mgmt_grp, name=policy_name)
        mgmt_rsaddrinst = RsAddrInst(mgmt_inbzone, tDn='uni/tn-mgmt/addrinst-'+policy_name+'inbaddr')
        mgmt_rsinbepg = RsInbEpg(mgmt_inbzone, tDn='uni/tn-mgmt/mgmtp-default/inb-'+args['in_band_management_epg'])

    if is_valid_key(args, 'out_of_band_management_epg'):
        mgmt_oobzone = OoBZone(mgmt_grp, name=policy_name)
        mgmt_rsaddroobst = RsAddrInst(mgmt_oobzone, tDn='uni/tn-mgmt/addrinst-'+policy_name+'oobaddr')
        mgmt_rsoobbepg = RsOobEpg(mgmt_oobzone, tDn='uni/tn-mgmt/mgmtp-default/oob-'+args['out_of_band_management_epg'])


def create_ip_address_pool(tn_mgmt, policy_name, **args):
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    if is_valid_key(args,'in_band_management_epg'):
        fvns_addrinst = AddrInst(tn_mgmt, policy_name+'inbaddr', addr=args['in_band_gateway'])
        fvns_ucastaddrblk = UcastAddrBlk(fvns_addrinst, args['in_band_ip_address_from'], args['in_band_ip_address_to'])
    if is_valid_key(args, 'out_of_band_management_epg'):
        fvns_addrinst = AddrInst(tn_mgmt, policy_name+'oobaddr', addr=args['out_of_band_gateway'])
        fvns_ucastaddrblk = UcastAddrBlk(fvns_addrinst, args['out_of_band_ip_address_from'], args['out_of_band_ip_address_to'])


def create_infra_nodes(parent_mo, policy_name, fabric_nodes_id):
    mgmt_nodegrp = NodeGrp(parent_mo, policy_name)
    mgmt_rsgrp = RsGrp(mgmt_nodegrp, 'uni/infra/funcprof/grp-'+policy_name)
    for node_id in fabric_nodes_id:
        random_name = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
        infra_nodeblk = NodeBlk(mgmt_nodegrp, random_name, from_=node_id, to_=node_id)


class CreateNodeManagementAddress(CreateMo):

    def __init__(self):
        self.description = 'Create Node Management Address'
        self.tenant_required = True
        self.tenant = 'mgmt'
        self.policy_name = None
        super(CreateNodeManagementAddress, self).__init__()

    def set_cli_mode(self):
        super(CreateNodeManagementAddress, self).set_cli_mode()
        self.parser_cli.add_argument('policy_name', help='Policy Name')
        self.parser_cli.add_argument('-i', '--in_band_address', nargs=4, help='Specify In-Band IP Address info: In-Band Management EPG, In-Band Gateway with Mask and In-Band IP Addresses range ("from" and "to").')
        self.parser_cli.add_argument('-o', '--out_of_band_address', nargs=4, help='Specify Out-of-Band IP Address info: Out-Band Management EPG, Out-Band Gateway with Mask and Out-Band IP Addresses range ("from" and "to").')
        self.parser_cli.add_argument('-n', '--fabric_nodes_id', nargs='*', help='Select the Fabric Nodes: spines, leaf or apic.')

    def read_key_args(self):
        self.policy_name = self.args.pop('policy_name')

    def wizard_mode_input_args(self):
        self.args['policy_name'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def run_cli_mode(self):
        super(CreateNodeManagementAddress, self).run_cli_mode()
        if not self.delete:
            self.optional_args['in_band_management_epg'] = self.optional_args['in_band_address'][0]
            self.optional_args['in_band_gateway'] = self.optional_args['in_band_address'][1]
            self.optional_args['in_band_ip_address_from'] = self.optional_args['in_band_address'][2]
            self.optional_args['in_band_ip_address_to'] = self.optional_args['in_band_address'][3]

            self.optional_args['out_of_band_management_epg'] = self.optional_args['out_of_band_address'][0]
            self.optional_args['out_of_band_gateway'] = self.optional_args['out_ofband_address'][1]
            self.optional_args['out_of_band_ip_address_from'] = self.optional_args['out_of_band_address'][2]
            self.optional_args['out_of_band_ip_address_to'] = self.optional_args['out_of_band_address'][3]

    def delete_mo(self):
        if self.check_if_mo_exist('uni/infra/funcprof/grp-', self.policy_name, Grp, description='Managed Node Connectivity Group', return_false=True):
            self.mo.delete()
            self.commit_change()
        if self.check_if_mo_exist('uni/infra/mgmtnodegrp-', self.policy_name, NodeGrp, description='The managed node group', return_false=True):
            self.mo.delete()
            self.commit_change()
        if self.check_if_mo_exist('uni/tn-'+self.tenant+'/addrinst-', self.policy_name+'inbaddr', AddrInst, description='', return_false=True):
            self.mo.delete()
            self.commit_change()
        if self.check_if_mo_exist('uni/tn-'+self.tenant+'/addrinst-', self.policy_name+'oobaddr', AddrInst, description='', return_false=True):
            self.mo.delete()
            self.commit_change()
        sys.exit()

    def main_function(self):

        self.look_up_mo('uni/infra/funcprof','')
        create_node_management_address(self.mo, self.policy_name, optional_args=self.optional_args)
        if is_valid_key(self.optional_args, 'in_band_management_epg') or is_valid_key(self.optional_args, 'out_of_band_management_epg'):
            self.commit_change()
            self.check_if_tenant_exist()
            create_ip_address_pool(self.mo, self.policy_name, optional_args=self.optional_args)
        if is_valid_key(self.optional_args, 'fabric_nodes_id'):
            self.commit_change()
            self.look_up_mo('uni/infra', '')
            create_infra_nodes(self.mo, self.policy_name, self.optional_args['fabric_nodes_id'])

if __name__ == '__main__':
    mo = CreateNodeManagementAddress()


