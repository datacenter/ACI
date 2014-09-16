import createFilter
from empty import *

class Moss(CreateMo):
    """
    Create a Filter
    """
    def __init__(self):
        self.description = 'Create Filters'
        self.tenant_required = True
        self.filters = None
        super(Moss, self).__init__()

    def set_argparse(self):
        super(Moss, self).set_argparse()
        self.parser_cli = self.subparsers.add_parser(
            'cli', help='Not Support.'
        )

    def set_cli_mode(self):
        pass

    def run_cli_mode(self):
        print 'CLI mode is not supported in this method. Please try Yaml mode or Wizard mode.'
        sys.exit()

    def run_yaml_mode(self):
        super(Moss, self).run_yaml_mode()

    def run_wizard_mode(self):
        super(Moss, self).run_wizard_mode()
        self.filters = add_mos('Add a Filter', createFilter.input_key_args, createFilter.input_optional_args)

    def bon_MOS(self):
        pass

if __name__ == '__main__':
    mo = Moss()