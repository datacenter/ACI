from cobra.model.mgmt import InstP, Subnet, RsOoBCons
from createMo import *

DEFAULT_QOS = 'unspecified'

QOS_CHOICES = ['level1', 'level2', 'level3', 'unspecified']


def input_key_args(msg='\nPlease the External management Entity instance:'):
    print msg
    return input_raw_input("The external management entity instance profile name", required=True)


def input_consumed_out_of_band_contract():
    return {'name': input_raw_input('Contract name', required=True),
            'prio': input_options('Prio(QoS Class)', DEFAULT_QOS, QOS_CHOICES)}


def input_subnet():
    return input_raw_input('Subnet IP with Mask', required=True)


def input_optional_args():
    args = {}
    # args['consumed_contracts'] = read_add_mos_args(add_mos('Add a consumed Out-of-Band contract', input_consumed_out_of_band_contract))
    # args['subnets'] = read_add_mos_args(add_mos('Add a sunbet', input_subnet))
    args['prio'], = input_options('Prio(QoS Class)', DEFAULT_QOS, QOS_CHOICES),
    args['consumed_contract'] = input_consumed_out_of_band_contract()
    args['subnet'] = input_subnet()
    return args


def create_external_management_entity_instance(parent_mo, profile_name, **args):
    """Create an external management entity instance profile. The instance profiles of external management entities can communicate with nodes that are part of out-of-band management endpoint group. To enable this communication, a contract is required between the instance profile and the out-of-band management endpoint group. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    # Create mo
    mgmt_instp = InstP(parent_mo, profile_name,
                       prio=get_value(args, 'prio', DEFAULT_QOS))
    if is_valid_key(args, 'consumed_contract'):
        mgmt_rsoobcons = RsOoBCons(mgmt_instp, args['consumed_contract']['name'],
                                   prio=get_value(args['consumed_contract'], 'prio', DEFAULT_QOS))
    if is_valid_key(args, 'subnet'):
        mgmt_subnet = Subnet(mgmt_instp, args['subnet'])


class CreateExternalManagementEntityInstance(CreateMo):

    def __init__(self):
        self.description = 'Create an external management entity instance profile. The instance profiles of external management entities can communicate with nodes that are part of out-of-band management endpoint group. To enable this communication, a contract is required between the instance profile and the out-of-band management endpoint group. '
        self.tenant_required = True
        self.tenant = 'mgmt'
        self.profile_name = None
        super(CreateExternalManagementEntityInstance, self).__init__()

    def set_cli_mode(self):
        super(CreateExternalManagementEntityInstance, self).set_cli_mode()
        self.parser_cli.add_argument('profile_name', help='The external management entity instance profile name.')
        self.parser_cli.add_argument('-Q', '--QoS_class', dest='prio', default= DEFAULT_QOS, choices=QOS_CHOICES, help='The priority level of a sub application running behind an endpoint group.')
        self.parser_cli.add_argument('-c', '--consumed_contract', nargs=2, help='Contract name and QoS class.')
        self.parser_cli.add_argument('-s', '--subnet', help='The external subnet to be imported.')

    def read_key_args(self):
        self.profile_name = self.args.pop('profile_name')

    def wizard_mode_input_args(self):
        self.args['profile_name'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def run_cli_mode(self):
        super(CreateExternalManagementEntityInstance, self).run_cli_mode()
        if not self.delete:
            self.optional_args['consumed_contract'] = {'name': self.optional_args['consumed_contract'][0],
                                                       'prio': self.optional_args['consumed_contract'][1]}

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-mgmt/extmgmt-default/instp-', self.profile_name, InstP, description='The external management entity instance profile')
        super(CreateExternalManagementEntityInstance, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.look_up_mo('uni/tn-mgmt/extmgmt-default', '')
        create_external_management_entity_instance(self.mo, self.profile_name, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateExternalManagementEntityInstance()


