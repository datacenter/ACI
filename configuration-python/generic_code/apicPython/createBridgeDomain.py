from cobra.model.fv import BD, Ctx, RsCtx, Subnet

from createPrivateNetwork import input_key_args as input_private_network
from createMo import *


def input_key_args(msg='\nPlease Specify Bridge Domain:', delete_function=False):
    print msg
    args = [input_raw_input("Bridge Domain", required=True)]
    if not delete_function:
        args.append(input_raw_input("Subnet IP", required=True))
    else:
        args.extend([None, None])
    return args


def createBridgeDomain(fv_tenant, bridge_domain, subnet_ip, private_network):
    """Create a Bridge Domain. A private layer 2 bridge domain (BD) consists of a set of physical or virtual ports. Each bridge domain must be linked to a context and have at least one subnet. """
    # Create a bridge domain
    fv_bd = BD(fv_tenant, bridge_domain)

    # Create a subnet
    fv_subnet = Subnet(fv_bd, subnet_ip)

    # Connect the bridge domain to a network
    fv_rsctx = RsCtx(fv_bd, tnFvCtxName=private_network)


class createBridgeDomain(CreateMo):

    def __init__(self):
        self.description = 'Create a Bridge Domain. A private layer 2 bridge domain (BD) consists of a set of physical or virtual ports. Each bridge domain must be linked to a context and have at least one subnet. '
        self.tenant_required = True
        self.bridge_domain = None
        self.subnet_ip = None
        self.private_network = None
        super(createBridgeDomain, self).__init__()

    def set_cli_mode(self):
        super(createBridgeDomain, self).set_cli_mode()
        self.parser_cli.add_argument('bridge_domain', help='Bridge Domain Name')
        self.parser_cli.add_argument('subnet_ip', help='Subnet IP')
        self.parser_cli.add_argument('private_network', help='Private Network')

    def read_key_args(self):
        self.bridge_domain = self.args.pop('bridge_domain')
        self.subnet_ip = self.args.pop('subnet_ip')
        self.private_network = self.args.pop('private_network')

    def wizard_mode_input_args(self):
        self.args['bridge_domain'], self.args['subnet_ip'] = input_key_args(delete_function=self.delete)
        self.args['private_network'] = input_private_network('')

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/BD-', self.bridge_domain, BD, description='Bridge Domain')
        super(createBridgeDomain, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/ctx-', self.private_network, Ctx, description='Private Network')
        parent_mo = self.check_if_tenant_exist()
        createBridgeDomain(parent_mo, self.bridge_domain, self.subnet_ip, self.private_network)

if __name__ == '__main__':
    bridge_domain = createBridgeDomain()