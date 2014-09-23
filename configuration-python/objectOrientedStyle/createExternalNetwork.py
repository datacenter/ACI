from createRoutedOutside import input_key_args as input_routed_outside
from cobra.model.l3ext import Out, InstP, Subnet

from createMo import *

DEFAULT_QOS = 'unspecified'

QOS_CHOICES = ['level1', 'level2', "level3", "unspecified"]


def input_key_args(msg='\nPlease External Network Instance Profile:'):
    print msg
    return input_raw_input("EPG Network Name", required=True)


def input_optional_args():
    args = {}
    args['prio'] = input_options('QoS Class', DEFAULT_QOS, QOS_CHOICES)
    args['subnet_ip'] = input_raw_input('Subnet IP Address')
    return args


def create_external_network(l3ext_out, external_network, **args):
    """The external network instance profile represents a group of external subnets that have the same security behavior. These subnets inherit contract profiles applied to the parent instance profile. Each subnet can also associate to route control profiles, which defines the routing behavior for that subnet. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    l3ext_instp = InstP(l3ext_out, external_network,
                        prio=get_value(args,'prio', 'unspecified'))
    if 'subnet_ip' in args.keys() and is_valid(args['subnet_ip']):
        l3ext_subnet = Subnet(l3ext_instp, args['subnet_ip'])


class CreateExternalNetwork(CreateMo):

    def __init__(self):
        self.description = 'The external network instance profile represents a group of external subnets that have the same security behavior. These subnets inherit contract profiles applied to the parent instance profile. Each subnet can also associate to route control profiles, which defines the routing behavior for that subnet. '
        self.tenant_required = True
        self.routed_outside = None
        self.external_network = None
        super(CreateExternalNetwork, self).__init__()

    def set_cli_mode(self):
        super(CreateExternalNetwork, self).set_cli_mode()
        self.parser_cli.add_argument('routed_outside', help='The name for the policy controlling connectivity to the outside.')
        self.parser_cli.add_argument('external_network', help='The name of the layer 3 external network instance profile.')
        self.parser_cli.add_argument('-Q', '--QoS_class', dest='prio', default= DEFAULT_QOS, choices=QOS_CHOICES, help='The priority level of a sub application running behind an endpoint group.')
        self.parser_cli.add_argument('-s', '--subnet_ip', help='The network visibility of the domain.')

    def read_key_args(self):
        self.routed_outside = self.args.pop('routed_outside')
        self.external_network = self.args.pop('external_network')

    def wizard_mode_input_args(self):
        self.args['routed_outside'] = input_routed_outside(msg='\nPlease External Network Instance Profile:')
        self.args['external_network'] = input_key_args('')
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-' + self.routed_outside + '/instP-', self.external_network, InstP, description='External Netwrok')
        super(CreateExternalNetwork, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.check_if_tenant_exist()
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/out-', self.routed_outside, Out, description='The policy')
        create_external_network(self.mo, self.external_network, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateExternalNetwork()