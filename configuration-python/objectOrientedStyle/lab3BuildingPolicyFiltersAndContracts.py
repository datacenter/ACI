import createFilter
import createContract
from createMo import *

class lab3BuildingPolicyFiltersAndContracts(CreateMo):
    """
    Create Filters and Contracts
    """
    def __init__(self):
        self.description = 'Create Filters and Contracts'
        self.tenant_required = True
        self.filters = []
        self.contracts = []
        super(lab3BuildingPolicyFiltersAndContracts, self).__init__()

    def set_argparse(self):
        super(lab3BuildingPolicyFiltersAndContracts, self).set_argparse()
        self.parser_cli = self.subparsers.add_parser(
            'cli', help='Not Support.'
        )

    def delete_mo(self):
        print 'Delete method is not supported in this function.'
        sys.exit()

    def set_cli_mode(self):
        pass


    def run_cli_mode(self):
        print 'CLI mode is not supported in this method. Please try Yaml mode or Wizard mode.'
        sys.exit()

    def run_yaml_mode(self):
        super(lab3BuildingPolicyFiltersAndContracts, self).run_yaml_mode()
        self.filters = self.args['filters']
        self.contracts = self.args['contracts']

    def read_opt_args(self):
        pass

    def wizard_mode_input_args(self):
        filters = add_mos('Add a Filter', createFilter.input_key_args, createFilter.input_optional_args)
        contracts = add_mos('Add a Contract', createContract.input_key_args, createContract.input_optional_args)
        for filter in filters:
            self.filters.append({'name': filter['key_args'], 'optional_args': filter['opt_args']})
        for contract in contracts:
            self.contracts.append({'name': contract['key_args'], 'optional_args': contract['opt_args']})

    def main_function(self):
        fv_tenant = self.check_if_tenant_exist()
        for filter in self.filters:
            createFilter.create_filter(fv_tenant, filter['name'], optional_args=filter['optional_args'])
        for contract in self.contracts:
            createContract.create_contract(fv_tenant, contract['name'], optional_args=contract['optional_args'])

if __name__ == '__main__':
    mo = lab3BuildingPolicyFiltersAndContracts()