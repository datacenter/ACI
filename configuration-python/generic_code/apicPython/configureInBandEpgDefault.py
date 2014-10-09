from cobra.model.mgmt import InB, RsMgmtBD
from cobra.model.fv import RsProv, RsCons, RsProtBy

from createMo import *


DEFAULT_ENCAP = ''
DEFAULT_QOS = 'unspecified'
DEFAULT_BRIDGE_DOMAIN = ''
DEFAULT_MATCH_TYPE = 'AtleastOne'

QOS_CHOICES = ['level1', 'level2', 'level3', DEFAULT_QOS]
CONTRACT_TYPE_CHOICES = ['provided', 'consumed', 'taboo']
MATCH_TYPE_CHOICES = ['All', 'AtleastOne', "AtmostOne", "None"]


def input_key_args(msg='\nPlease Specify In Band EPG:'):
    print msg
    return input_raw_input("In Band EPG Name", required=True)


def input_contract_optional_args(contract=''):
    args = {}
    args['prio'], = input_options('Prio(QoS Class)', DEFAULT_QOS, QOS_CHOICES),
    if contract == 'provided':
        args['match_type'] = input_options('Match Type', DEFAULT_MATCH_TYPE, MATCH_TYPE_CHOICES, )
    return args


def input_optional_args():
    args = {}
    args['encap'] = input_raw_input('Access Encapsulation', default=DEFAULT_ENCAP)
    args['prio'] = input_options('Prio(QoS Class)', DEFAULT_QOS, QOS_CHOICES)
    args['bridge_domain'] = input_raw_input('Bridge Domain')

    if input_yes_no('Add a default Provided contract', default='no'):
        args['provided_contract'] = {}
        args['provided_contract']['name'] = 'default'
        args['provided_contract']['optional_args'] = input_contract_optional_args('provided')

    if input_yes_no('Add a default consumed contract', default='no'):
        args['consumed_contract'] = {}
        args['consumed_contract']['name'] = 'default'
        args['consumed_contract']['optional_args'] = input_contract_optional_args('consumed')

    if input_yes_no('Add a default Taboo contract', default='no'):
        args['taboo_contract'] = {}
        args['taboo_contract']['name'] = 'default'
    return args


def configureIn_band_epg_default(parent_mo, in_band_epg, **args):
    """The in-band management endpoint group, which consists of switches (leaves/spines) and APICs. Each node in the group is assigned an IP address that is dynamically allocated from the address pool associated with the corresponding in-band management zone. The allocated IP address is then configured as the in-band management access IP address on the corresponding node. Any host that is part of another endpoint group can communicate with the nodes in the in-band management endpoint group using contacts. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    fv_inb = InB(parent_mo, in_band_epg,
                 encap=get_value(args, 'encap', DEFAULT_ENCAP),
                 prio=get_value(args, 'prio', DEFAULT_QOS))
    if is_valid_key(args, 'bridge_domain'):
        mgmt_rsmgmtbd = RsMgmtBD(fv_inb, tnFvBDName=args['bridge_domain'])

    if is_valid_key(args, 'provided_contract'):
        fv_rsprov = RsProv(fv_inb, args['provided_contract']['name'],
                           prio=get_value(args['provided_contract']['optional_args'], 'prio', DEFAULT_QOS) if is_valid_key(args['provided_contract'], 'optional_args') else DEFAULT_QOS,
                           matchT=get_value(args['provided_contract']['optional_args'], 'match_type', DEFAULT_MATCH_TYPE) if is_valid_key(args['provided_contract'], 'optional_args') else DEFAULT_MATCH_TYPE
        )

    if is_valid_key(args, 'consumed_contract'):
        fv_rscons = RsCons(fv_inb, args['consumed_contract']['name'],
                           prio=get_value(args['consumed_contract']['optional_args'], 'prio', DEFAULT_QOS),
        )

    if is_valid_key(args, 'taboo_contract'):
        fv_rsprotby = RsProtBy(fv_inb, args['taboo_contract']['name'])


class ConfigureInBandEpgDefault(CreateMo):

    def __init__(self):
        self.description = 'The in-band management endpoint group, which consists of switches (leaves/spines) and APICs. Each node in the group is assigned an IP address that is dynamically allocated from the address pool associated with the corresponding in-band management zone. The allocated IP address is then configured as the in-band management access IP address on the corresponding node. Any host that is part of another endpoint group can communicate with the nodes in the in-band management endpoint group using contacts. '
        self.tenant_required = True
        self.tenant = 'mgmt'
        self.in_band_epg = None
        super(ConfigureInBandEpgDefault, self).__init__()

    def set_cli_mode(self):
        super(ConfigureInBandEpgDefault, self).set_cli_mode()
        self.parser_cli.add_argument('in_band_epg', help='The in-band management endpoint group name.')
        self.parser_cli.add_argument('-e', '--encap', default= DEFAULT_ENCAP, help='Access Encapsulation')
        self.parser_cli.add_argument('-Q', '--QoS_class', dest='prio', default= DEFAULT_QOS, choices=QOS_CHOICES, help='The priority level of a sub application running behind an endpoint group.')
        self.parser_cli.add_argument('-b', '--bridge_domain', default= DEFAULT_BRIDGE_DOMAIN, help='Relationship to management BD.')
        self.parser_cli.add_argument('-p', '--provided_contract', nargs=3, help='Labels the EPG as a provider in the contract. It accepts three arguments: the contract name, QoS class and match type.')
        self.parser_cli.add_argument('-c', '--consumed_contract', nargs=2, help='Labels the EPG as a provider in the contract. It accepts two arguments: the contract name and QoS class.')
        self.parser_cli.add_argument('-t', '--taboo_contract', nargs=1, help='Labels the EPG as a provider in the contract. It accepts only one argument: the contract name.')

    def run_cli_mode(self):
        self.set_host_user_password()
        self.read_key_args()
        self.read_opt_args()
        self.apic_login()
        if is_valid_key(self.optional_args, 'provided_contract'):
            self.optional_args['provided_contract']={
                'name':self.optional_args['provided_contract'][0],
                'optional_args':{'prio':self.optional_args['provided_contract'][1],
                                  'match_type':self.optional_args['provided_contract'][2]}}
        if is_valid_key(self.optional_args, 'consumed_contract'):
            self.optional_args['consumed_contract']={
                'name':self.optional_args['consumed_contract'][0],
                'optional_args':{'prio':self.optional_args['consumed_contract'][1]}}
        if is_valid_key(self.optional_args, 'taboo_contract'):
            self.optional_args['taboo_contract']={
                'name':self.optional_args['taboo_contract'][0]}

    def read_key_args(self):
        self.in_band_epg = self.args.pop('in_band_epg')

    def wizard_mode_input_args(self):
        self.args['in_band_epg'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-mgmt/mgmtp-default/inb-', self.in_band_epg, InB, description='In-Band EPG')
        super(ConfigureInBandEpgDefault, self).delete_mo()

    def main_function(self):
        self.look_up_mo('uni/tn-mgmt/mgmtp-default','')
        configureIn_band_epg_default(self.mo, self.in_band_epg, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = ConfigureInBandEpgDefault()


