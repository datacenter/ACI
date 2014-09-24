from cobra.model import Module
from createMo import *

DEFAULT_CONSTANT = 'unspecified'

CHOICES = []


def input_key_args(msg='\nPlease Specify Xxxx:'):
    print msg
    return input_raw_input("Xxxx Name", required=True)


def input_optional_args():
    args = {}
    args['xxxx_name'], = input_raw_input('Xxxx Name', default=DEFAULT_CONSTANT),
    return args


def create_xxxx(parent_mo, mo, **args):
    """Create a Xxxx"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    module = Module(parent_mo, mo)


class CreateXxxx(CreateMo):

    def __init__(self):
        self.description = 'Create a Xxxx'
        self.tenant_required = True # (or False)
        super(CreateXxxx, self).__init__()

    def set_cli_mode(self):
        super(CreateXxxx, self).set_cli_mode()
        self.parser_cli.add_argument('mo', help='Xxxx_Name')
        self.parser_cli.add_argument('-o', '--opt1', default= DEFAULT_CONSTANT, choices=CHOICES, help='Xxxx name')

    def read_key_args(self):
        self.xxxx = self.args.pop('xxxx')

    def wizard_mode_input_args(self):
        self.args['xxxx'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('Xxxx_Path', self.xxxx, Module, description='Xxxx')
        super(CreateXxxx, self).delete_mo()

    def main_function(self):
        # Query a tenant
        parent_mo = self.check_if_tenant_exist()
        create_xxxx(self.mo, self.xxxx, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateXxxx()


