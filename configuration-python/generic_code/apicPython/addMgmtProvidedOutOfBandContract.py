from cobra.model.mgmt import RsOoBProv

from createMo import *


DEFAULT_QOS = 'unspecified'

QOS_CHOICES = ['level1', 'level2', 'level3', 'unspecified']


def input_key_args(msg='\nPlease the Provided Out-of-Band contract:'):
    print msg
    return input_raw_input("Contract Name", required=True)


def input_optional_args():
    args = {}
    args['prio'], = input_options('Prio(QoS Class)', DEFAULT_QOS, QOS_CHOICES),
    return args


def add_mgmt_provided_out_of_band_contract(parent_mo, contract, **args):
    """The out-of-band management endpoint group. This is the out-of-band contract provider when a relationship to the out-of-band binary contract profile is established. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    mgmt_rsoobprov = RsOoBProv(parent_mo, contract,
                               prio=get_value(args, 'prio', DEFAULT_QOS))


class AddMgmtProvidedOutOfBandContract(CreateMo):

    def __init__(self):
        self.description = 'The out-of-band management endpoint group. This is the out-of-band contract provider when a relationship to the out-of-band binary contract profile is established. '
        self.tenant_required = True
        self.tenant = 'mgmt'
        super(AddMgmtProvidedOutOfBandContract, self).__init__()

    def set_cli_mode(self):
        super(AddMgmtProvidedOutOfBandContract, self).set_cli_mode()
        self.parser_cli.add_argument('contract', help='The Out-of-Band contract name.')
        self.parser_cli.add_argument('-Q', '--QoS_class', dest='prio', default= DEFAULT_QOS, choices=QOS_CHOICES, help='The priority level of a sub application running behind an endpoint group.')

    def read_key_args(self):
        self.contract = self.args.pop('contract')

    def wizard_mode_input_args(self):
        self.args['contract'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-mgmt/mgmtp-default/oob-default/rsooBProv-', self.contract, RsOoBProv, description='The Out-of-Band contract')
        super(AddMgmtProvidedOutOfBandContract, self).delete_mo()

    def main_function(self):
        self.look_up_mo('uni/tn-mgmt/mgmtp-default/oob-default','')
        add_mgmt_provided_out_of_band_contract(self.mo, self.contract, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = AddMgmtProvidedOutOfBandContract()


