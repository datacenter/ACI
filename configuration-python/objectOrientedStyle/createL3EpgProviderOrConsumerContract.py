from cobra.model.fv import RsProv, RsCons
from cobra.model.l3ext import Out, InstP

from createRoutedOutside import input_key_args as input_routed_outside
from createExternalNetwork import input_key_args as input_external_network_name

from createMo import *

DEFAULT_QOS = 'unspecified'
DEFAULT_MTACH_TYPE = 'AtleastOne'

CONTRACT_TYPE_CHOICES = ['provided', 'consumed']
QOS_CHOICES = ['level1', 'level2', 'level3', 'unspecified']
MATCH_TYPE_CHOICES = ['All', 'AtleastOne', "AtmostOne", "None"]


def input_key_args(msg='\nPlease Specify the L3 EPG Contract:'):
    print msg
    args = []
    args.append(input_options("Contract type", '', CONTRACT_TYPE_CHOICES, required=True))
    args.append(input_raw_input("Contract Name", default='default'))
    return args


def input_optional_args(contract_type):
    args = {}
    args['prio'] = input_options('QoS Class', DEFAULT_QOS, QOS_CHOICES)
    print contract_type.lower(), contract_type.lower()=='provided'
    if contract_type.lower() == 'provided':
        args['match_type'] = input_options('Match Type', DEFAULT_MTACH_TYPE, MATCH_TYPE_CHOICES)
    return args


def create_L3_epg_provider_or_consumer_contract(l3ext_instp, contract_type, contract, **args):
    """Labels the EPG as a provider/consumer in the contract. A contract defines what can be communicated along with the protocols and ports on which a provider and consumer are allowed to communicate."""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    if contract_type.lower() == 'consumed':
        fv_l3epg_cont = RsCons(l3ext_instp, contract,
                               prio=get_value(args, 'prio', 'unspecified'))

    elif contract_type.lower() == 'provided':
        fv_l3epg_cont = RsProv(l3ext_instp, contract,
                               prio=get_value(args, 'prio', 'unspecified'),
                               matchT=get_value(args, 'match_type', 'AtleastOne'))
    else:
        print 'Invalid Contract Type ' + contract_type + '. Contract_type is either \"consumed\" or \"provided\".'
        sys.exit()
    return fv_l3epg_cont


class CreateL3EpgProviderOrConsumerContract(CreateMo):

    def __init__(self):
        self.description = 'Labels the EPG as a provider/consumer in the contract. A contract defines what can be communicated along with the protocols and ports on which a provider and consumer are allowed to communicate.'
        self.tenant_required = True
        self.routed_outside = None
        self.external_network = None
        self.contract_type = None
        self.external_network = None
        super(CreateL3EpgProviderOrConsumerContract, self).__init__()

    def set_cli_mode(self):
        super(CreateL3EpgProviderOrConsumerContract, self).set_cli_mode()
        self.parser_cli.add_argument('routed_outside', help='The name for the policy controlling connectivity to the outside.')
        self.parser_cli.add_argument('external_network', help='The name of the layer 3 external network instance profile.')
        self.parser_cli.add_argument('contract_type', choices=CONTRACT_TYPE_CHOICES, help='Defind the contract type.')
        self.parser_cli.add_argument('contract', help='The provider/consumer contract name')
        self.parser_cli.add_argument('-Q', '--QoS_class', dest='prio', default= DEFAULT_QOS, choices=QOS_CHOICES, help='The priority level of a sub application running behind an endpoint group.')
        self.parser_cli.add_argument('-m', '--match_type', default= DEFAULT_MTACH_TYPE, choices=MATCH_TYPE_CHOICES, help='The matched EPG type. For provider only.')

    def read_key_args(self):
        self.routed_outside = self.args.pop('routed_outside')
        self.external_network = self.args.pop('external_network')
        self.contract_type = self.args.pop('contract_type')
        self.contract = self.args.pop('contract')

    def wizard_mode_input_args(self):
        self.args['routed_outside'] = input_routed_outside(msg='\nPlease Specify the L3 EPG Contract:')
        self.args['external_network'] = input_external_network_name('')
        self.args['contract_type'], self.args['contract'] = input_key_args('')
        if not self.delete:
            self.args['optional_args'] = input_optional_args(self.args['contract_type'])

    def delete_mo(self):
        if self.contract_type.lower() == 'provided':
            self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/instP-' + self.external_network + '/rsprov-', self.contract, RsProv, description='L3 EPG Provider Contract')
        elif self.contract_type.lower() == 'consumed':
            self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/instP-' + self.external_network + '/rscons-', self.contract, RsCons, description='L3 EPG Consumer Contract')
        super(CreateL3EpgProviderOrConsumerContract, self).delete_mo()

    def main_function(self):
        self.check_if_tenant_exist()
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-', self.routed_outside, Out, description='The policy')
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/instP-', self.external_network, InstP, description='External Netwrok')
        create_L3_epg_provider_or_consumer_contract(self.mo, self.contract_type, self.contract, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateL3EpgProviderOrConsumerContract()