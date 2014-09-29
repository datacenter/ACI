from cobra.model.vz import OOBBrCP, Subj,RsSubjFiltAtt
from createMo import *

DEFAULT_SCOPE = 'context'
DEFAULT_QOS = 'unspecified'

SCOPE_CHOICES = ['application-profile', 'context', 'global', 'tenant']
QOS_CHOICES = ['level1', 'level2', 'level3', 'unspecified']


def input_key_args(msg='\nPlease Specify the Out-of-Band Contract:'):
    print msg
    return input_raw_input("The name of the out-of-band binary contract profile.", required=True)


def input_optional_args():
    args = {}
    args['scope'], = input_options('Scope', DEFAULT_SCOPE, SCOPE_CHOICES),
    args['prio'], = input_options('Prio(QoS Class)', DEFAULT_QOS, QOS_CHOICES),
    return args


def create_out_of_band_contract(parent_mo, contract, **args):
    """Create an out-of-band binary contract profile. The out-of-band binary contract profiles can only be provided by an out-of-band endpoint group and can only be consumed by the external prefix set. A regular endpoint group cannot provide or consume an out-of-band contract profile. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    vz_oobbfrcp = OOBBrCP(parent_mo, contract,
                          scope=get_value(args, 'scope', DEFAULT_SCOPE),
                          prio=get_value(args, 'prio', DEFAULT_QOS))
    vz_subj = Subj(vz_oobbfrcp, contract,
                   prio=get_value(args, 'prio', DEFAULT_QOS))
    vz_rssubjfiltatt = RsSubjFiltAtt(vz_subj, 'default')


class CreateOutOfBandContract(CreateMo):

    def __init__(self):
        self.description = 'Create an out-of-band binary contract profile. The out-of-band binary contract profiles can only be provided by an out-of-band endpoint group and can only be consumed by the external prefix set. A regular endpoint group cannot provide or consume an out-of-band contract profile. '
        self.tenant_required = True
        self.tenant = 'mgmt'
        self.contract = None
        super(CreateOutOfBandContract, self).__init__()

    def set_cli_mode(self):
        super(CreateOutOfBandContract, self).set_cli_mode()
        self.parser_cli.add_argument('contract', help='The name of an out-of-band binary contract profile. ')
        self.parser_cli.add_argument('-s', '--scope', default= DEFAULT_SCOPE, choices=SCOPE_CHOICES, help='Represents the scope of this contract.')
        self.parser_cli.add_argument('-Q', '--QoS_class', dest='prio', default= DEFAULT_QOS, choices=QOS_CHOICES, help='The priority level of a sub application running behind an endpoint group.')

    def read_key_args(self):
        self.contract = self.args.pop('contract')

    def wizard_mode_input_args(self):
        self.args['contract'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-'+self.tenant+'/oobbrc-', self.contract, OOBBrCP, description='The out-of-band binary contract profil')
        super(CreateOutOfBandContract, self).delete_mo()

    def main_function(self):
        self.check_if_tenant_exist()
        create_out_of_band_contract(self.mo, self.contract, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateOutOfBandContract()


