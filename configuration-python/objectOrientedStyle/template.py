from cobra.model import Module
from createMo import *

DEFAULT_CONSTANT = 'unspecified'

CHOICES = []

def input_key_args(msg='\nPlease Specify XXXX:'):
    print msg
    return input_raw_input("XXXX Name", required=True)


def input_optional_args():
    args = {}
    args['xxxx_name'], = input_raw_input('xxxx Name', default=DEFAULT_CONSTANT),
    return args


def create_xxxx(parent_mo, mo, **args):
    """Create a mo"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    module = Module(parent_mo, mo)


class CreateXxxx(CreateMo):
    """
    Create a Xxxx
    """
    def __init__(self):
        self.description = 'Create a Xxxx'
        self.tenant_required = True # (or False)
        super(CreateXxxx, self).__init__()

    def set_cli_mode(self):
        super(CreateXxxx, self).set_cli_mode()
        self.parser_cli.add_argument('mo', help='Xxxx Name')
        self.parser_cli.add_argument('-o', '--opt1', default= DEFAULT_CONSTANT, choices=CHOICES, help='Some xxxx')

    def run_cli_mode(self):
        super(CreateXxxx, self).run_cli_mode()
        self.mo = self.args.pop('mo')
        self.optional_args = self.args

    def run_yaml_mode(self):
        super(CreateXxxx, self).run_yaml_mode()
        self.mo = self.args['mo']
        self.optional_args = self.args['optional_args']

    def run_wizard_mode(self):
        super(CreateXxxx, self).run_wizard_mode()
        self.mo = input_key_args()
        if not self.delete:
            self.optional_args = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('Xxxx Path', self.mo, Module, description='Xxxx')
        super(CreateXxxx, self).delete_mo()

    def main_function(self):
        # Query a tenant
        parent_mo = self.check_if_tenant_exist()
        create_xxxx(parent_mo, self.mo, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateXxxx()