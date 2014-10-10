from cobra.model.l3ext import Out, RsEctx
from cobra.model.bgp import ExtP as bgpExtP
from cobra.model.ospf import ExtP as ospfExtP
from cobra.model.tag import Inst

from createMo import *


DEFAULT_NONE = ''
DEFAULT_NO = 'no'
DEFAULT_OSPF_AREA_ID = 'None'

CHOICES = []


def input_key_args(msg='\nPlease Specify Routed Outside Network:'):
    print msg
    return input_raw_input("Routed Outside Network Name", required=True)


def input_optional_args():
    args = {}
    args['private_network'], = input_raw_input('Private Network', default=DEFAULT_NONE),
    args['tags'] = input_raw_input('Tags', default=DEFAULT_NONE)
    args['bgp'] = input_yes_no('Apply BGP (default:'+DEFAULT_NO+')')
    args['ospf'] = input_yes_no('Apply OSPF (default:'+DEFAULT_NO+')')
    if args['ospf']:
        args['ospf_area_id'] = input_options('OSPF Area ID,', DEFAULT_OSPF_AREA_ID, '', num_accept=True)
    return args


def create_routed_outside(fv_tenant, routed_outside_name, **args):
    """Create a Routed Outside policy"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    l3ext_out = Out(fv_tenant, routed_outside_name)
    if 'private_network' in args.keys():
        l3ext_rsectx = RsEctx(l3ext_out, tnFvCtxName=args['private_network'])
    if 'bgp' in args.keys() and args['bgp']:
        bgp_extp = bgpExtP(l3ext_out)
    if 'ospf' in args.keys() and args['ospf']:
        ospf_extp = ospfExtP(l3ext_out, areaId='0.0.0.' + str(get_value(args, 'ospf_area_id', '1')))
    if 'tags' in args.keys() and is_valid(args['tags']):
        tag_inst = Inst(l3ext_out, args['tags'])
    return l3ext_out


class CreateRoutedOutside(CreateMo):

    def __init__(self):
        self.description = 'The policy controlling connectivity to outside.'
        self.tenant_required = True
        self.routed_outside = None
        super(CreateRoutedOutside, self).__init__()

    def set_cli_mode(self):
        super(CreateRoutedOutside, self).set_cli_mode()
        self.parser_cli.add_argument('routed_outside', help='The name for the policy controlling connectivity to the outside.')
        self.parser_cli.add_argument('-p', '--private_network', help='The target name of the relation that defines which private network (layer 3 context or VRF) is associated with the external endpoint group networks (layer 3 instance profile).')
        self.parser_cli.add_argument('-t', '--tags', help='A tag allows you to group multiple objects by a descriptive name.')
        self.parser_cli.add_argument('-B', '--bgp', action='store_const', const=True, default=null_function, help='When created, this profile indicates that IBGP will be configured for the endpoint groups in this external network.')
        self.parser_cli.add_argument('-O', '--ospf', action='store_const', const=True, default=null_function, help='The OSPF external profile information.')
        self.parser_cli.add_argument('-i', '--ospf_area_id', help='The OSPF Area ID.')

    def read_key_args(self):
        self.routed_outside = self.args.pop('routed_outside')

    def wizard_mode_input_args(self):
        self.args['routed_outside'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-', self.routed_outside, Out, description='The policy')
        super(CreateRoutedOutside, self).delete_mo()

    def main_function(self):
        self.check_if_tenant_exist()
        create_routed_outside(self.mo, self.routed_outside, optional_args=self.optional_args)


if __name__ == '__main__':
    mo = CreateRoutedOutside()