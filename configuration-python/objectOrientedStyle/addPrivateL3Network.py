from cobra.model.fv import Ctx
from createMo import *


def input_key_args(msg='\nPlease Specify Private Network:'):
    print msg
    return input_raw_input("Private Network Name", required=True)


def input_optional_args():
    args = {'private_network': input_raw_input('Private Network Name')[0]}
    return args


def create_private_network(parent_mo, private_network):
    """Create a Private Network"""
    fv_ctx = Ctx(parent_mo, private_network)


class CreatePrivateNetwork(CreateMo):

    def __init__(self):
        self.description = 'Create a Private Network'
        self.tenant_required = True
        self.private_network = None
        super(CreatePrivateNetwork, self).__init__()

    def set_cli_mode(self):
        super(CreatePrivateNetwork, self).set_cli_mode()
        self.parser_cli.add_argument('private_network', help='Private Network Name')

    def read_key_args(self):
        self.private_network = self.args.pop('private_network')

    def wizard_mode_input_args(self):
        self.args['private_network'] = input_key_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/ctx-', self.private_network, Ctx, description='Private Network')
        super(CreatePrivateNetwork, self).delete_mo()

    def main_function(self):
        # Query a tenant
        parent_mo = self.check_if_tenant_exist()
        create_private_network(parent_mo, self.private_network)

if __name__ == '__main__':
    private_network = CreatePrivateNetwork()