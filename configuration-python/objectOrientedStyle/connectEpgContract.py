from cobra.model.fv import AEPg, RsCons, RsProv
from cobra.model.vz import BrCP
from createMo import *

CONTRACT_TYPE_CHOICES = ['provided', 'consumed']


def input_key_args(msg='\nPlease Specify EPG and Contract:'):
    print msg
    args = []
    args.append(input_raw_input("EPG Name", required=True))
    args.append(input_raw_input("Contract Name", required=True))
    args.append(input_options("Contract Type", '', CONTRACT_TYPE_CHOICES, required=True))
    return args


def connect_epg_contract(fv_aepg, contract_name, contract_type):
    """Apply Contract to EPG. The consumer relation to a binary contract profile."""
    # Check the contract type, consumed or provided.
    if contract_type.lower() == 'consumed':
        # Add a consumed contract to EPG
        fv_rscons = RsCons(fv_aepg, contract_name)
    elif contract_type.lower() == 'provided':
        # Add a provided contract to EPG
        fv_rsprov = RsProv(fv_aepg, contract_name)
    else:
        print 'Invalid Contract Type ' + contract_type + '. Contract_type is either \"consumed\" or \"provided\".'
        return

class ConnectEpgContract(CreateMo):

    def __init__(self):
        self.description = 'Apply Contract to EPG. The consumer relation to a binary contract profile.'
        self.tenant_required = True
        self.epg = None
        self.contract_name = None
        self.contract_type = None
        super(ConnectEpgContract, self).__init__()

    def set_cli_mode(self):
        super(ConnectEpgContract, self).set_cli_mode()
        self.parser_cli.add_argument('application', help='Application Name')
        self.parser_cli.add_argument('epg', help='Application EPG Name')
        self.parser_cli.add_argument('contract_name', help='Contract Name')
        self.parser_cli.add_argument('contract_type', help='Contract Type', choices=CONTRACT_TYPE_CHOICES)

    def read_key_args(self):
        self.application = self.args.pop('application')
        self.epg = self.args.pop('epg')
        self.contract_name = self.args.pop('contract_name')
        self.contract_type = self.args.pop('contract_type')

    def wizard_mode_input_args(self):
        self.args['application'] = self.input_application_name()
        self.args['epg'], self.args['contract_name'], self.args['contract_type'] = input_key_args()

    def delete_mo(self):
        path = 'uni/tn-' + self.tenant + '/ap-' + self.application + '/epg-' + self.epg
        if self.contract_type.lower() == 'consumed':
            path += '/rscons-'
            module = RsCons
        elif self.contract_type.lower() == 'provided':
            path += '/rsprov-'
            module = RsProv
        else:
            print 'Invalid Contract Type ' + self.contract_type + '. Contract_type is either \"consumed\" or \"provided\".'
            sys.exit()
        self.check_if_mo_exist(path, self.contract_name, module)
        super(ConnectEpgContract, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/brc-', self.contract_name, BrCP, description='Contract')
        fv_aepg = self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-' + self.application + '/epg-', self.epg, AEPg, description='EPG')
        connect_epg_contract(fv_aepg, self.contract_name, self.contract_type)

if __name__ == '__main__':
    mo = ConnectEpgContract()