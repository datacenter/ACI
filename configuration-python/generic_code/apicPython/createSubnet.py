from cobra.model.fv import Subnet, BD

from createMo import *

DEFAULT_CONSTANT = 'unspecified'

CHOICES = []


def input_key_args(msg='\nPlease Specify Subnet:'):
    print msg
    args = []
    args.append(input_raw_input("Bridge Domain", required=True))
    args.append(input_raw_input("Subnet IP", required=True))
    return args


def create_subnet(fv_bd, subnet):
    """Configures the Endpoint Group (EPG) as a portion of the network that shares the same subnet address. The context defined IP address space can consist of multiple subnets. Those subnets are defined in one or more bridge domains that reference the corresponding context. Subnets can span multiple EPGs. """
    fv_subnet = Subnet(fv_bd, subnet)


class CreateSubnet(CreateMo):

    def __init__(self):
        self.description = 'Configures the Endpoint Group (EPG) as a portion of the network that shares the same subnet address. The context defined IP address space can consist of multiple subnets. Those subnets are defined in one or more bridge domains that reference the corresponding context. Subnets can span multiple EPGs. '
        self.tenant_required = True
        self.bridge_domain = None
        self.subnet = None
        super(CreateSubnet, self).__init__()

    def set_cli_mode(self):
        super(CreateSubnet, self).set_cli_mode()
        self.parser_cli.add_argument('bridge_domain', help='The Bridge Domain of the subnet')
        self.parser_cli.add_argument('subnet', help='The IP address and mask of the the default gateway.')

    def read_key_args(self):
        self.bridge_domain = self.args.pop('bridge_domain')
        self.subnet = self.args.pop('subnet')

    def wizard_mode_input_args(self):
        self.args['bridge_domain'] = input_key_args()
        self.args['subnet'] = input_key_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-'+self.tenant+'/BD-'+self.bridge_domain+'/subnet-['+self.subnet+']', module=Subnet, description='Subnet')
        super(CreateSubnet, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.check_if_tenant_exist()
        fv_bd = self.check_if_mo_exist('uni/tn-'+self.tenant+'/BD-', self.bridge_domain, BD, description='Bridge Domain', return_false=True, set_mo=False)
        if not fv_bd:
            fv_bd = BD(self.mo, self.bridge_domain)
        create_subnet(fv_bd, self.subnet)

if __name__ == '__main__':
    mo = CreateSubnet()
