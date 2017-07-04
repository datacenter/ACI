from cobra.model.vz import BrCP, Subj, RsSubjFiltAtt

from createMo import *


DEFAULT_SCOPE = 'context'
DEFAULT_REVERSE_FILTER_PORTS = 'true'
DEFAULT_QOS = 'unspecified'

SCOPE_CHOICES = ['application-profile', 'context', 'global', 'tenant']
REVERSE_FILTER_CHOICES = ['true', 'false']
QOS_CHOICES = ['level1', 'level2', 'level3', 'unspecified']


def input_key_args(msg='\nPlease specify the Contract:'):
    print msg
    return input_raw_input("Contract Name", required=True)


def input_filter():
    return input_raw_input("Filter Name", required=True)


def input_optional_args(contract):
    args = {}
    args['scope'] = input_options('Scope', DEFAULT_SCOPE, SCOPE_CHOICES)
    args['prio'] = input_options('Prio(QoS Class of Contract)', DEFAULT_QOS, QOS_CHOICES)
    args['subject'] = input_raw_input('Subject Name', default=contract.lower())
    args['reverse_filter_ports'] = input_options('Reverse Filter Ports', DEFAULT_REVERSE_FILTER_PORTS, REVERSE_FILTER_CHOICES)
    args['subject_prio'] = input_options('Prio(QoS Class of subject)', DEFAULT_QOS, QOS_CHOICES)
    args['filters'] = read_add_mos_args(add_mos('Add a filter to the subject', input_filter))

    return args


def add_filter_to_subject(vz_subj, filter):
    vz_rs_subj_filt_att = RsSubjFiltAtt(vz_subj, filter)


def create_contract_subject(vz_ct, contract, **args):
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    vz_subj = Subj(vz_ct,
                   get_value(args, 'subject', contract + '_subj'),
                   revFltPorts=str(get_value(args, 'reverse_filter_ports', DEFAULT_REVERSE_FILTER_PORTS)).lower(),
                   prio=get_value(args, 'subject_prio', DEFAULT_QOS))
    return vz_subj


def create_contract(fv_tenant, contract, **args):
    """Create a Contract"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create contract
    vz_ct = BrCP(fv_tenant, contract,
                 scope=get_value(args, 'scope', DEFAULT_SCOPE),
                 prio=get_value(args, 'prio', DEFAULT_QOS))
    return vz_ct


class CreateContract(CreateMo):
    """
    Create a Contract
    """
    def __init__(self):
        self.description = 'Create a Contract'
        self.tenant_required = True
        self.contract = None
        super(CreateContract, self).__init__()

    def set_cli_mode(self):
        super(CreateContract, self).set_cli_mode()
        self.parser_cli.add_argument('contract', help='Contract Name')
        self.parser_cli.add_argument('-s', '--scope', default= DEFAULT_SCOPE, choices=SCOPE_CHOICES, help='Represents the scope of this contract.')
        self.parser_cli.add_argument('-Q', '--QoS_class', dest='prio', default= DEFAULT_QOS, choices=QOS_CHOICES, help='The priority level of a sub application running behind an endpoint group.')
        self.parser_cli.add_argument('-n', '--subject', help='Name of a subject in the contract.')
        self.parser_cli.add_argument('-q', '--Subject_QoS_class', dest='subject_prio', default= DEFAULT_QOS, choices=QOS_CHOICES, help='The priority level of a sub application running behind an endpoint group.')
        self.parser_cli.add_argument('-r', '--reverse_filter_ports', default= DEFAULT_REVERSE_FILTER_PORTS, choices=REVERSE_FILTER_CHOICES, help='Enables the filter to apply on both ingress and egress traffic.')
        self.parser_cli.add_argument('-f', '--filters', help='The applied Filter.', nargs='+')

    def read_key_args(self):
        self.contract = self.args.pop('contract')

    def wizard_mode_input_args(self):
        self.args['contract'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args(self.args['contract'])

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-'+self.tenant+'/brc-', self.contract, BrCP, description='Contract')
        super(CreateContract, self).delete_mo()

    def main_function(self):
        # Query a tenant
        fv_tenant = self.check_if_tenant_exist()

        vz_ct = create_contract(fv_tenant, self.contract, optional_args=self.optional_args)

        # Add a subject to the contract
        if self.optional_args and is_valid_key(self.optional_args, 'subject'):

            vz_subj = create_contract_subject(vz_ct, self.contract, optional_args=self.optional_args)
            # Assign an existed filter to the subject
            if is_valid_key(self.optional_args, 'filters'):
                for filter in self.optional_args['filters']:
                    add_filter_to_subject(vz_subj, filter)


if __name__ == '__main__':
    mo = CreateContract()