from cobra.model.phys import DomP
from cobra.model.infra import RsVlanNs

from createMo import *

DEFAULT_VLAN_POOL = 'none'

VLAN_MODE_CHOICES = ['dynamic', 'static']


def input_key_args(msg='\nPlease Specify Physical Domain:'):
    print msg
    return input_raw_input("Physical Domain Name", required=True)


def input_optional_args():
    args = {}
    args['vlan_pool'] = input_raw_input('Vlan Name', default=DEFAULT_VLAN_POOL)
    if args['vlan_pool'] not in ['None', 'none', 'NONE', '']:
        args['vlan_mode'] = input_options("Vlan Mode", '', VLAN_MODE_CHOICES, required=True)
    return args


def create_physical_domain(uni, physical_domain, **args):
    """Create a Physical domain. Physical domain profile is a policy pertaining to single Physical Management domain that also corresponds to a single policy enforcement domain: representing the physical binding of Tenant/EPGs. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    phys_domp = DomP(uni, physical_domain)
    if 'vlan_pool' in args.keys() and 'vlan_mode' in args.keys():
        infra_rsvlanns = RsVlanNs(phys_domp, tDn='uni/infra/vlanns-[' + args['vlan_pool'] + ']-' + args['vlan_mode'])


class CreatePhysicalDomain(CreateMo):

    def __init__(self):
        self.description = 'Create a Physical domain. Physical domain profile is a policy pertaining to single Physical Management domain that also corresponds to a single policy enforcement domain: representing the physical binding of Tenant/EPGs. '
        self.physical_domain = None
        super(CreatePhysicalDomain, self).__init__()

    def set_cli_mode(self):
        super(CreatePhysicalDomain, self).set_cli_mode()
        self.parser_cli.add_argument('physical_domain', help='The name of the object.')
        self.parser_cli.add_argument('-v', '--vlan_pool', default= DEFAULT_VLAN_POOL, help='VLAN Pool name')
        self.parser_cli.add_argument('-m', '--vlan_mode', choices=VLAN_MODE_CHOICES, help='VLAN Pool Mode')

    def read_key_args(self):
        self.physical_domain = self.args.pop('physical_domain')

    def wizard_mode_input_args(self):
        self.args['physical_domain'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/phys-', self.physical_domain, DomP, description='Physical Domain')
        super(CreatePhysicalDomain, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.look_up_mo('uni/', '')
        create_physical_domain(self.mo, self.physical_domain, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreatePhysicalDomain()


