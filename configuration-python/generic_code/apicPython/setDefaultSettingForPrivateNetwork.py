from cobra.model.fv import Ctx, RsBgpCtxPol, RsOspfCtxPol, RsCtxToEpRet, RsCtxMonPol

from createMo import *

DEFAULT_POLICY = 'None'

CHOICES = []


def input_key_args(msg=''):
    print msg
    return input_raw_input("Private Network Name", required=True)


def input_optional_args():
    args = {}
    args['bgp_timer'] = input_raw_input("BGP Timers", default=DEFAULT_POLICY)
    args['ospf_timer'] = input_raw_input("OSPF Timers", default=DEFAULT_POLICY)
    args['end_point_retention_policy'] = input_raw_input("End Point Retention Policy", default=DEFAULT_POLICY)
    args['monitoring_policy'] = input_raw_input("Monitoring Policy", default=DEFAULT_POLICY)
    return args


def set_default_setting_for_private_network(fv_ctx, **args):
    """Set Default Setting For Private Network"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    if 'bgp_timer' in args and args['bgp_timer'] != '':
        fv_rsbgpctxpol = RsBgpCtxPol(fv_ctx, tnBgpCtxPolName='' if args['bgp_timer'] != None and args['bgp_timer'].lower() == 'none' else args['bgp_timer'])
    if 'ospf_timer' in args and args['ospf_timer'] != '':
        fv_rsospfctxpol = RsOspfCtxPol(fv_ctx, tnOspfCtxPolName='' if args['ospf_timer'] != None and args['ospf_timer'].lower() == 'none' else args['ospf_timer'])
    if 'end_point_retention_policy' in args and args['end_point_retention_policy'] != '':
        fv_rsctxtoepret = RsCtxToEpRet(fv_ctx, tnFvEpRetPolName='' if args['end_point_retention_policy'] != None and args['end_point_retention_policy'].lower() == 'none' else args['end_point_retention_policy'])
    if 'monitoring_policy' in args and args['monitoring_policy'] != '':
        fv_rsctxmonpol = RsCtxMonPol(fv_ctx, tnMonEPGPolName='' if args['monitoring_policy'] != None and args['monitoring_policy'].lower() == 'none' else args['monitoring_policy'])


class SetDefaultSettingForPrivateNetwork(CreateMo):

    def __init__(self):
        self.description = 'Set Default Setting For Private Network'
        self.tenant_required = True
        super(SetDefaultSettingForPrivateNetwork, self).__init__()

    def set_cli_mode(self):
        super(SetDefaultSettingForPrivateNetwork, self).set_cli_mode()
        self.parser_cli.add_argument('private_network', help='Private Network Name')
        self.parser_cli.add_argument('-B', '--BGP-Timer', dest='bgp_timer', help='A relation to the BGP timer policy. This is an internal object.')
        self.parser_cli.add_argument('-O', '--OSPF-Timer', dest='ospf_timer', help='A relation to the context-level OSPF timer policy. This is an internal object.')
        self.parser_cli.add_argument('-e', '--End-Point-Retention-Policy', dest='end_point_retention_policy', help='A relation to an endpoint retention policy. This is an internal object.')
        self.parser_cli.add_argument('-m', '--Monitoring-Policy', dest='monitoring_policy', help='A relation to the monitoring policy model for the endpoint group semantic scope. This is an internal object.')

    def read_key_args(self):
        self.private_network = self.args.pop('private_network')

    def wizard_mode_input_args(self):
        self.args['private_network'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/ctx-', self.private_network, Ctx, description='Private Network')
        self.optional_args['bgp_timer'] = 'none'
        self.optional_args['ospf_timer'] = 'none'
        self.optional_args['end_point_retention_policy'] = 'none'
        self.optional_args['monitoring_policy'] = 'none'
        set_default_setting_for_private_network(self.mo, optional_args=self.optional_args)

    def main_function(self):
        self.check_if_tenant_exist()
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/ctx-', self.private_network, Ctx, description='Private Network')
        set_default_setting_for_private_network(self.mo, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = SetDefaultSettingForPrivateNetwork()