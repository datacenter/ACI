from cobra.model.fv import Ctx, RsBgpCtxPol, RsOspfCtxPol, RsCtxMonPol
from cobra.model.dns import Lbl

from createMo import *

DEFAULT_ENFORCEMENT_PREFERENCE = 'enforced'

ENFORCEMENT_PREFERENCE_CHOICES = ['enforced', 'unenforced']


def input_key_args(msg='\nPlease Specify Private Network:'):
    print msg
    return input_raw_input("Private Network Name", required=True)


def input_optional_args():
    args = {'enforcement_preference': input_options('Policy Control Enforcement Preference', DEFAULT_ENFORCEMENT_PREFERENCE, ENFORCEMENT_PREFERENCE_CHOICES),
            'bgp_timers': input_raw_input('BGP Timers'),
            'ospf_timers': input_raw_input('OSPF Timers'),
            'monitoring_policy': input_raw_input('Monitoring Policy'),
            'dns_label': input_raw_input('DNS Label')}
    return args


def create_private_network(parent_mo, private_network, **args):
    """Create a Private Network. The private layer 3 network context that belongs to a specific tenant or is shared."""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    fv_ctx = Ctx(parent_mo, private_network,
                 pcEnfPref=get_value(args, 'enforcement_preference', DEFAULT_ENFORCEMENT_PREFERENCE))

    if is_valid_key(args, 'dns_label'):
        dns_lbl = Lbl(fv_ctx, args['dns_label'])

    if is_valid_key(args, 'bgp_timers'):
        fv_rsbgpctxpol = RsBgpCtxPol(fv_ctx, tnBgpCtxPolName=args['bgp_timers'])

    if is_valid_key(args, 'ospf_timers'):
        fv_rsospfctxpol = RsOspfCtxPol(fv_ctx, tnOspfCtxPolName=args['ospf_timers'])

    if is_valid_key(args, 'bgp_timers'):
        fv_rsctxmonpol = RsCtxMonPol(fv_ctx, tnMonEPGPolName=args['monitoring_policy'])

    return fv_ctx


class CreatePrivateNetwork(CreateMo):

    def __init__(self):
        self.description = 'Create a Private Network. The private layer 3 network context that belongs to a specific tenant or is shared.'
        self.tenant_required = True
        self.private_network = None
        super(CreatePrivateNetwork, self).__init__()

    def set_cli_mode(self):
        super(CreatePrivateNetwork, self).set_cli_mode()
        self.parser_cli.add_argument('private_network', help='A name for the network context.')
        self.parser_cli.add_argument('-e', '--enforcement_preference', default=DEFAULT_ENFORCEMENT_PREFERENCE, choices=ENFORCEMENT_PREFERENCE_CHOICES, help='Policy Control Enforcement Preference.')
        self.parser_cli.add_argument('-b', '--bgp_timers', help='A relation to the monitoring policy model for the endpoint group semantic scope. This is an internal object.')
        self.parser_cli.add_argument('-o', '--ospf_timers', help='A relation to the context-level OSPF timer policy. This is an internal object.')
        self.parser_cli.add_argument('-m', '--monitoring_policy', help='A relation to the BGP timer policy. This is an internal object.')
        self.parser_cli.add_argument('-d', '--dns_label', help='DNS Label')

    def read_key_args(self):
        self.private_network = self.args.pop('private_network')

    def wizard_mode_input_args(self):
        self.args['private_network'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/ctx-', self.private_network, Ctx, description='Private Network')
        super(CreatePrivateNetwork, self).delete_mo()

    def main_function(self):
        # Query a tenant
        parent_mo = self.check_if_tenant_exist()
        create_private_network(parent_mo, self.private_network, optional_args=self.optional_args)

if __name__ == '__main__':
    private_network = CreatePrivateNetwork()